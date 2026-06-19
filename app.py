import streamlit as st
import tempfile
import base64
from pdf_generator import generate_pdf

st.set_page_config(
    page_title="Medical Bill Generator",
    page_icon="🏥",
    layout="centered"
)

st.title("🏥 Medical Bill Generator")
st.markdown("Fill in the details below to generate an official medical bill PDF.")

# ── Patient Info ────────────────────────────────────────────────────────────
st.subheader("Patient Details")

col1, col2 = st.columns([3, 1])
with col1:
    patient_name = st.text_input("Patient Name")
with col2:
    age = st.number_input("Age", min_value=1, max_value=120, step=1, value=25)

doctor_name = st.text_input("Doctor Name")

col3, col4 = st.columns(2)
with col3:
    from_date = st.date_input("From Date")
with col4:
    to_date = st.date_input("To Date")

# ── Logo (optional) ─────────────────────────────────────────────────────────
st.subheader("Hospital Logo (Optional)")
logo_file = st.file_uploader(
    "Upload a small logo — it will appear in the top-right corner",
    type=["png", "jpg", "jpeg"]
)

# ── Bills ───────────────────────────────────────────────────────────────────
st.subheader("Bills")

num_bills = st.number_input(
    "Number of Bills", min_value=1, max_value=50, value=1, step=1
)

bills = []
for i in range(int(num_bills)):
    c1, c2 = st.columns(2)
    with c1:
        bill_date = st.date_input(f"Bill Date {i+1}", key=f"date_{i}")
    with c2:
        amount = st.number_input(
            f"Amount {i+1} (₹)", min_value=0.0, step=0.01, key=f"amt_{i}"
        )
    bills.append((bill_date.strftime("%d/%m/%Y"), amount))

total_amount = sum(amt for _, amt in bills)
st.markdown(f"### Total Amount: ₹ {total_amount:,.0f}")

# ── Generate ─────────────────────────────────────────────────────────────────
if st.button("📄 Generate PDF", type="primary", use_container_width=True):

    if not patient_name.strip():
        st.error("Please enter the patient name.")
        st.stop()

    if not doctor_name.strip():
        st.error("Please enter the doctor name.")
        st.stop()

    # Save logo to temp file if provided
    logo_path = None
    if logo_file:
        ext = "." + logo_file.name.rsplit(".", 1)[-1]
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
        tmp.write(logo_file.read())
        tmp.close()
        logo_path = tmp.name

    # Generate PDF
    pdf_path = generate_pdf(
        patient_name=patient_name.strip(),
        age=int(age),
        doctor_name=doctor_name.strip(),
        from_date=from_date.strftime("%d/%m/%Y"),
        to_date=to_date.strftime("%d/%m/%Y"),
        bills=bills,
        total_amount=total_amount,
        logo_path=logo_path
    )

    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    st.success("✅ PDF generated successfully!")

    # ── Download button ──────────────────────────────────────────────────────
    st.download_button(
        label="⬇️ Download PDF",
        data=pdf_bytes,
        file_name=f"{patient_name.strip().replace(' ', '_')}_Medical_Bills.pdf",
        mime="application/pdf",
        use_container_width=True
    )

    # ── Inline Preview ───────────────────────────────────────────────────────
    st.subheader("Preview")
    b64 = base64.b64encode(pdf_bytes).decode("utf-8")
    pdf_display = f"""
        <iframe
            src="data:application/pdf;base64,{b64}"
            width="100%"
            height="700px"
            style="border: 1px solid #ddd; border-radius: 6px;"
        ></iframe>
    """
    st.markdown(pdf_display, unsafe_allow_html=True)