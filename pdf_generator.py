import os
import tempfile
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


def generate_pdf(
    patient_name,
    age,
    doctor_name,
    from_date,
    to_date,
    bills,
    total_amount,
    logo_path=None
):
    pdf_path = tempfile.mktemp(suffix=".pdf")
    page_width, page_height = A4

    margin_left = 40 * mm
    margin_right = 40 * mm
    content_width = page_width - margin_left - margin_right

    c = canvas.Canvas(pdf_path, pagesize=A4)

    y = page_height - 20 * mm  # Start near top

    # ── LOGO (optional, top-right corner) ──────────────────────────────────
    logo_size = 18 * mm
    if logo_path:
        try:
            c.drawImage(
                logo_path,
                page_width - margin_right - logo_size,
                y - logo_size,
                width=logo_size,
                height=logo_size,
                preserveAspectRatio=True,
                mask="auto"
            )
        except Exception:
            pass

    # ── TITLE ───────────────────────────────────────────────────────────────
    c.setFont("Times-Bold", 16)
    title = "MEDICAL BILLS"
    title_width = c.stringWidth(title, "Times-Bold", 16)
    title_x = (page_width - title_width) / 2
    c.drawString(title_x, y, title)

    # Underline
    c.setLineWidth(0.8)
    c.line(title_x, y - 1, title_x + title_width, y - 1)

    y -= 8 * mm

    # ── DURATION ────────────────────────────────────────────────────────────
    c.setFont("Times-Roman", 11)
    duration_text = f"Duration: FROM:{from_date}  To  {to_date}"
    duration_width = c.stringWidth(duration_text, "Times-Roman", 11)
    c.drawString((page_width - duration_width) / 2, y, duration_text)

    y -= 8 * mm

    # ── TABLE ───────────────────────────────────────────────────────────────
    col1 = content_width * 0.55
    col2 = content_width * 0.22
    col3 = content_width * 0.23
    col_widths = [col1 + col2, col3]   # for 2-col rows
    col_widths_3 = [col1 * 0.25, col1 * 0.40 + col2 * 0.40, col3 + col1 * 0.35 + col2 * 0.20]

    # We'll build rows manually using the canvas for precise control
    row_height = 10 * mm
    header_height = 9 * mm

    table_x = margin_left
    table_right = page_width - margin_right
    table_w = content_width

    def draw_cell(x, y, w, h, text, font="Times-Roman", size=11,
                  align="LEFT", bold=False, bg=None, pad_left=3):
        if bg:
            c.setFillColor(bg)
            c.rect(x, y - h, w, h, fill=1, stroke=0)
            c.setFillColor(colors.black)
        c.setFont(font if not bold else "Times-Bold", size)
        text_y = y - h + (h - size * 0.352778 * mm) / 2 + 0.5 * mm
        if align == "CENTER":
            tw = c.stringWidth(str(text), font if not bold else "Times-Bold", size)
            c.drawString(x + (w - tw) / 2, text_y, str(text))
        elif align == "RIGHT":
            tw = c.stringWidth(str(text), font if not bold else "Times-Bold", size)
            c.drawString(x + w - tw - pad_left * mm, text_y, str(text))
        else:
            c.drawString(x + pad_left * mm, text_y, str(text))

    def draw_border(x, y, w, h):
        c.setStrokeColor(colors.black)
        c.setLineWidth(0.5)
        c.rect(x, y - h, w, h, fill=0, stroke=1)

    # ----- Row 1: Patient name + Age -----
    rh = row_height
    name_col_w = table_w * 0.75
    age_col_w = table_w * 0.25

    draw_cell(table_x, y, name_col_w, rh,
              f"Name of the patient: {patient_name}", size=11)
    draw_cell(table_x + name_col_w, y, age_col_w, rh,
              f"AGE: {age}", size=11, align="CENTER")
    draw_border(table_x, y, name_col_w, rh)
    draw_border(table_x + name_col_w, y, age_col_w, rh)
    y -= rh

    # ----- Row 2: Doctor name (full width) -----
    draw_cell(table_x, y, table_w, rh,
              f"Name of the doctor: {doctor_name}", size=11)
    draw_border(table_x, y, table_w, rh)
    y -= rh

    # ----- Header row: S.NO | Bill date | Bill Amount -----
    sno_w = table_w * 0.20
    date_w = table_w * 0.40
    amt_w = table_w * 0.40

    draw_cell(table_x, y, sno_w, header_height,
              "S.NO", bold=True, align="CENTER", size=11)
    draw_cell(table_x + sno_w, y, date_w, header_height,
              "Bill date", bold=True, align="CENTER", size=11)
    draw_cell(table_x + sno_w + date_w, y, amt_w, header_height,
              "Bill Amount", bold=True, align="CENTER", size=11)
    draw_border(table_x, y, sno_w, header_height)
    draw_border(table_x + sno_w, y, date_w, header_height)
    draw_border(table_x + sno_w + date_w, y, amt_w, header_height)
    y -= header_height

    # ----- Bill rows -----
    for i, (date, amount) in enumerate(bills, start=1):
        draw_cell(table_x, y, sno_w, rh, str(i), align="CENTER", size=11)
        draw_cell(table_x + sno_w, y, date_w, rh, date, align="CENTER", size=11)
        draw_cell(table_x + sno_w + date_w, y, amt_w, rh,
                  f"{amount:,.0f}", align="CENTER", size=11)
        draw_border(table_x, y, sno_w, rh)
        draw_border(table_x + sno_w, y, date_w, rh)
        draw_border(table_x + sno_w + date_w, y, amt_w, rh)
        y -= rh

    # ----- Total row (full width) -----
    total_text = f"Total Amount:  {total_amount:,.0f}"
    draw_cell(table_x, y, table_w, rh, total_text,
              bold=True, align="CENTER", size=12)
    draw_border(table_x, y, table_w, rh)

    c.save()
    return pdf_path