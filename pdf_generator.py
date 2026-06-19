from reportlab.platypus import *
from reportlab.lib import colors

def generate_pdf(
    patient,
    age,
    doctor,
    bills,
    total,
    logo_path=None
):
    pdf = SimpleDocTemplate("medical_bill.pdf")

    content = []

    if logo_path:
        content.append(
            Image(
                logo_path,
                width=120,
                height=60
            )
        )

    content.append(
        Paragraph("MEDICAL BILLS")
    )

    content.append(
        Paragraph(f"Patient: {patient}")
    )

    content.append(
        Paragraph(f"Age: {age}")
    )

    content.append(
        Paragraph(f"Doctor: {doctor}")
    )

    data = [["S.No", "Date", "Amount"]]

    for i, (date, amount) in enumerate(bills):
        data.append([i+1, date, amount])

    data.append(["", "Total", total])

    table = Table(data)

    table.setStyle([
        ("GRID", (0,0), (-1,-1), 1, colors.black)
    ])

    content.append(table)

    pdf.build(content)

    return "medical_bill.pdf"