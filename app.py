import streamlit as st
from pdf_generator import generate_pdf
import tempfile

st.set_page_config(page_title="Medical Bill Generator", layout="centered")

st.title("Medical Bill Generator")

patient_name = st.text_input("Patient Name")
age = st.number_input("Age", min_value=1, step=1)
doctor_name = st.text_input("Doctor Name")

col1, col2 = st.columns(2)

with col1:
    from_date = st.date_input("From Date")

with col2:
    to_date = st.date_input("To Date")

logo_file = st.file_uploader("Hospital Logo", type=["png", "jpg", "jpeg"])

st.subheader("Bills")

num_bills = st.number_input("Number of Bills", min_value=1, value=1)

bills = []

for i in range(int(num_bills)):
    c1, c2 = st.columns(2)

    with c1:
        bill_date = st.date_input(f"Bill Date {i+1}", key=f"date{i}")

    with c2:
        amount = st.number_input(f"Amount {i+1}", min_value=0.0, key=f"amt{i}")

    bills.append((bill_date.strftime("%d/%m/%Y"), amount))

total_amount = sum(amount for _, amount in bills)

st.markdown(f"### Total Amount: ₹ {total_amount:,.0f}")

if st.button("Generate PDF"):

    if not patient_name:
        st.error("Enter patient name")
        st.stop()

    if not doctor_name:
        st.error("Enter doctor name")
        st.stop()

    logo_path = None

    if logo_file:
        ext = "." + logo_file.name.split(".")[-1]
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
        temp_file.write(logo_file.read())
        temp_file.close()
        logo_path = temp_file.name

    pdf_path = generate_pdf(
        patient_name,
        age,
        doctor_name,
        from_date.strftime("%d/%m/%Y"),
        to_date.strftime("%d/%m/%Y"),
        bills,
        total_amount,
        logo_path
    )

    with open(pdf_path, "rb") as f:
        st.download_button(
            "📄 Download PDF",
            f,
            file_name=f"{patient_name}_Medical_Bills.pdf",
            mime="application/pdf"
        )

    st.success("PDF Generated Successfully")