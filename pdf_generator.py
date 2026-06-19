from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


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

    pdf_path = "medical_bill.pdf"

    pdf = SimpleDocTemplate(
        pdf_path,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    content = []

    # Optional Logo
    if logo_path:
        try:
            logo = Image(
                logo_path,
                width=120,
                height=70
            )
            content.append(logo)
            content.append(Spacer(1, 10))
        except Exception:
            pass

    # Title
    content.append(
        Paragraph(
            "<b>MEDICAL BILLS</b>",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 10))

    # Duration
    content.append(
        Paragraph(
            f"<b>Duration:</b> FROM: {from_date} To {to_date}",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 10))

    # Patient Details
    content.append(
        Paragraph(
            f"Name of the patient: <b>{patient_name}</b>    AGE: <b>{age}</b>",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 5))

    content.append(
        Paragraph(
            f"Name of the doctor: <b>{doctor_name}</b>",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 15))

    # Table Header
    table_data = [
        ["S.NO", "Bill Date", "Bill Amount"]
    ]

    # Bill Rows
    for i, (date, amount) in enumerate(bills, start=1):
        table_data.append([
            str(i),
            str(date),
            f"{amount:.0f}"
        ])

    table = Table(
        table_data,
        colWidths=[60, 220, 120]
    )

    table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ])
    )

    content.append(table)

    content.append(Spacer(1, 20))

    # Total Amount
    content.append(
        Paragraph(
            f"<b>Total Amount: {total_amount:,.0f}</b>",
            styles["Heading3"]
        )
    )

    pdf.build(content)

    return pdf_path