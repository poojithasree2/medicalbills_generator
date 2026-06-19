from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Table,
    TableStyle,
    Image,
    Spacer
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
        rightMargin=30,
        leftMargin=30,
        topMargin=20,
        bottomMargin=20
    )

    styles = getSampleStyleSheet()

    content = []

    # Small Logo (Top Left)
    if logo_path:
        try:
            logo = Image(
                logo_path,
                width=35,
                height=35
            )
            content.append(logo)
        except:
            pass

    # Title
    content.append(
        Paragraph(
            "<para align='center'><b><u>MEDICAL BILLS</u></b></para>",
            styles["Title"]
        )
    )

    # Duration
    content.append(
        Paragraph(
            f"<para align='center'>Duration: FROM:{from_date} To {to_date}</para>",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 10))

    table_data = []

    # Patient Row
    table_data.append([
        f"Name of the patient:{patient_name}",
        "",
        f"AGE:{age}"
    ])

    # Doctor Row
    table_data.append([
        f"Name of the doctor:{doctor_name}",
        "",
        ""
    ])

    # Header
    table_data.append([
        "S.NO",
        "Bill date",
        "Bill Amount"
    ])

    # Bills
    for i, (date, amount) in enumerate(bills, start=1):
        table_data.append([
            str(i),
            str(date),
            f"{amount:.0f}"
        ])

    # Total Row
    table_data.append([
        f"Total Amount: {total_amount:,.0f}",
        "",
        ""
    ])

    table = Table(
        table_data,
        colWidths=[140, 140, 140]
    )

    table.setStyle(
        TableStyle([

            # Grid
            ("GRID", (0, 0), (-1, -1), 1, colors.black),

            # Merge patient row middle cell
            ("SPAN", (0, 1), (1, 1)),

            # Merge doctor row
            ("SPAN", (0, 1), (2, 1)),

            # Merge total row
            ("SPAN", (0, -1), (2, -1)),

            # Header row
            ("FONTNAME", (0, 2), (-1, 2), "Helvetica-Bold"),

            ("ALIGN", (0, 0), (-1, -1), "CENTER"),

            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

            ("ALIGN", (0, 0), (0, 1), "LEFT"),

            ("ALIGN", (0, -1), (-1, -1), "CENTER"),

            ("FONTSIZE", (0, 0), (-1, -1), 11),

            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),

            ("TOPPADDING", (0, 0), (-1, -1), 10),
        ])
    )

    content.append(table)

    pdf.build(content)

    return pdf_path