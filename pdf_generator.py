from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER


def generate_pdf(patient_name, age, doctor_name, from_date, to_date, bills, total_amount, logo_path=None):

    pdf_path = "medical_bill.pdf"

    pdf = SimpleDocTemplate(
        pdf_path,
        rightMargin=60,
        leftMargin=60,
        topMargin=30,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "title",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
        fontName="Times-Bold"
    )

    normal_center = ParagraphStyle(
        "normal_center",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontName="Times-Roman",
        fontSize=10
    )

    elements = []

    # LOGO
    if logo_path:
        try:
            logo = Image(logo_path, width=60, height=60)
            logo.hAlign = "CENTER"
            elements.append(logo)
        except:
            pass

    # TITLE
    elements.append(Paragraph("MEDICAL BILLS", title_style))
    elements.append(Spacer(1, 8))

    elements.append(Paragraph(f"Duration: {from_date} to {to_date}", normal_center))
    elements.append(Spacer(1, 12))

    # =========================
    # CLEAN PATIENT INFO BOX
    # =========================
    patient_box = Table([[
        f"Patient Name: {patient_name}   |   Age: {age}   |   Doctor: {doctor_name}"
    ]], colWidths=[480])

    patient_box.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1.2, colors.black),
        ("BACKGROUND", (0, 0), (-1, -1), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, -1), "Times-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("PADDING", (0, 0), (-1, -1), 10),
    ]))

    elements.append(patient_box)
    elements.append(Spacer(1, 15))

    # =========================
    # BILL TABLE
    # =========================
    data = [
        ["S.NO", "Bill Date", "Bill Amount"]
    ]

    for i, (date, amount) in enumerate(bills, start=1):
        data.append([str(i), date, f"₹ {amount:,.0f}"])

    # TOTAL ROW
    data.append(["", "TOTAL AMOUNT", f"₹ {total_amount:,.0f}"])

    table = Table(data, colWidths=[80, 200, 200])

    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.8, colors.black),

        # Header styling
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkgrey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Times-Bold"),

        # Alignment
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

        # Font size
        ("FONTSIZE", (0, 0), (-1, -1), 11),

        # Total row bold
        ("FONTNAME", (0, -1), (-1, -1), "Times-Bold"),
        ("BACKGROUND", (0, -1), (-1, -1), colors.lightgrey),
    ]))

    elements.append(table)

    pdf.build(elements)

    return pdf_path