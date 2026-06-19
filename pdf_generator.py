import tempfile
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


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

    # Tighter margins so table is wide and clear
    margin_left = 25 * mm
    margin_right = 25 * mm
    content_width = page_width - margin_left - margin_right

    c = canvas.Canvas(pdf_path, pagesize=A4)
    y = page_height - 22 * mm

    # ── LOGO (top-right, small) ─────────────────────────────────────────────
    logo_size = 16 * mm
    if logo_path:
        try:
            c.drawImage(
                logo_path,
                page_width - margin_right - logo_size,
                y - logo_size + 4 * mm,
                width=logo_size,
                height=logo_size,
                preserveAspectRatio=True,
                mask="auto"
            )
        except Exception:
            pass

    # ── TITLE ───────────────────────────────────────────────────────────────
    font_size_title = 15
    c.setFont("Times-Bold", font_size_title)
    title = "MEDICAL BILLS"
    tw = c.stringWidth(title, "Times-Bold", font_size_title)
    tx = (page_width - tw) / 2
    c.drawString(tx, y, title)
    c.setLineWidth(0.8)
    c.line(tx, y - 1.5, tx + tw, y - 1.5)

    y -= 8 * mm

    # ── DURATION ────────────────────────────────────────────────────────────
    c.setFont("Times-Roman", 11)
    dur = f"Duration: FROM:{from_date}  To  {to_date}"
    dw = c.stringWidth(dur, "Times-Roman", 11)
    c.drawString((page_width - dw) / 2, y, dur)

    y -= 7 * mm

    # ── HELPERS ─────────────────────────────────────────────────────────────
    rh = 10 * mm   # standard row height
    fs = 11        # font size

    def cell_text(x, cy, w, h, text, bold=False, align="LEFT", pad=3):
        font = "Times-Bold" if bold else "Times-Roman"
        c.setFont(font, fs)
        text_y = cy - h + (h - fs * 0.352778 * mm) / 2 + 0.5 * mm
        if align == "CENTER":
            tw2 = c.stringWidth(str(text), font, fs)
            c.drawString(x + (w - tw2) / 2, text_y, str(text))
        elif align == "RIGHT":
            tw2 = c.stringWidth(str(text), font, fs)
            c.drawString(x + w - tw2 - pad * mm, text_y, str(text))
        else:
            c.drawString(x + pad * mm, text_y, str(text))

    def border(x, cy, w, h):
        c.setStrokeColor(colors.black)
        c.setLineWidth(0.5)
        c.rect(x, cy - h, w, h, fill=0, stroke=1)

    lx = margin_left
    tw_full = content_width

    # ── ROW 1: Patient name | AGE ────────────────────────────────────────────
    name_w = tw_full * 0.75
    age_w  = tw_full * 0.25
    cell_text(lx,           y, name_w, rh, f"Name of the patient: {patient_name}")
    cell_text(lx + name_w,  y, age_w,  rh, f"AGE: {age}", align="CENTER")
    border(lx,          y, name_w, rh)
    border(lx + name_w, y, age_w,  rh)
    y -= rh

    # ── ROW 2: Doctor name (full width) ─────────────────────────────────────
    cell_text(lx, y, tw_full, rh, f"Name of the doctor: {doctor_name}")
    border(lx, y, tw_full, rh)
    y -= rh

    # ── HEADER ROW ──────────────────────────────────────────────────────────
    sno_w  = tw_full * 0.18
    date_w = tw_full * 0.41
    amt_w  = tw_full * 0.41
    cell_text(lx,                    y, sno_w,  rh, "S.NO",        bold=True, align="CENTER")
    cell_text(lx + sno_w,            y, date_w, rh, "Bill date",   bold=True, align="CENTER")
    cell_text(lx + sno_w + date_w,   y, amt_w,  rh, "Bill Amount", bold=True, align="CENTER")
    border(lx,                   y, sno_w,  rh)
    border(lx + sno_w,           y, date_w, rh)
    border(lx + sno_w + date_w,  y, amt_w,  rh)
    y -= rh

    # ── BILL ROWS ────────────────────────────────────────────────────────────
    for i, (date, amount) in enumerate(bills, start=1):
        cell_text(lx,                   y, sno_w,  rh, str(i),             align="CENTER")
        cell_text(lx + sno_w,           y, date_w, rh, date,               align="CENTER")
        cell_text(lx + sno_w + date_w,  y, amt_w,  rh, f"{amount:,.0f}",   align="CENTER")
        border(lx,                  y, sno_w,  rh)
        border(lx + sno_w,          y, date_w, rh)
        border(lx + sno_w + date_w, y, amt_w,  rh)
        y -= rh

    # ── TOTAL ROW ────────────────────────────────────────────────────────────
    c.setFont("Times-Bold", fs)
    total_text = f"Total Amount:  {total_amount:,.0f}"
    cell_text(lx, y, tw_full, rh, total_text, bold=True, align="CENTER")
    border(lx, y, tw_full, rh)

    c.save()
    return pdf_path