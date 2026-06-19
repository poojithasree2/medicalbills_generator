import streamlit as st
from pdf_generator import generate_pdf
import tempfile

st.set_page_config(
    page_title="Medical Bill Generator",
    layout="centered"
)

st.title("Medical Bill Generator")

# Patient Details
patient_name = st.text_input("Patient Name")
age = st.number_input("Age", min_value=1, step=1)
doctor_name = st.text_input("Doctor Name")

# Duration
col1, col2 = st.columns(2)

with col1:
    from_date = st.date_input("From Date")

with col2:
    to_date = st.date_input("To Date")

# Optional Logo
logo_file = st.file_uploader(
    "Upload Logo (Optional)",
    type=["png", "jpg", "jpeg"]
)

st.subheader("Bills")

num_bills = st.number_input(
    "Number of Bills",
    min_value=1,
    value=1,
    step=1
)

bills = []

for i in range(num_bills):
    c1, c2 = st.columns(2)

    with c1:
        bill_date = st.date_input(
            f"Bill Date {i+1}",
            key=f"date_{i}"
        )

    with c2:
        amount = st.number_input(
            f"Amount {i+1}",
            min_value=0.0,
            step=1.0,
            key=f"amount_{i}"
        )

    bills.append((str(bill_date), amount))

# Total
total_amount = sum(amount for _, amount in bills)

st.markdown(f"### Total Amount: ₹ {total_amount:,.2f}")

# Generate PDF
if st.button("Generate PDF"):

    logo_path = None

    if logo_file is not None:

        extension = "." + logo_file.name.split(".")[-1]

        temp_logo = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension
        )

        temp_logo.write(logo_file.read())
        temp_logo.close()

        logo_path = temp_logo.name

    pdf_path = generate_pdf(
        patient_name=patient_name,
        age=age,
        doctor_name=doctor_name,
        from_date=str(from_date),
        to_date=str(to_date),
        bills=bills,
        total_amount=total_amount,
        logo_path=logo_path
    )

    with open(pdf_path, "rb") as pdf_file:
        st.download_button(
            label="Download PDF",
            data=pdf_file,
            file_name="Medical_Bills.pdf",
            mime="application/pdf"
        )

    st.success("PDF Generated Successfully!")