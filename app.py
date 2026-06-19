import streamlit as st
import tempfile
import base64
import os
from pdf_generator import generate_pdf

st.set_page_config(
    page_title="Medical Bill Generator",
    page_icon="🏥",
    layout="centered"
)

st.title("🏥 Medical Bill Generator")

# ── Patient Info ─────────────────────────────────────────────────────────────
st.subheader("Patient Details")

patient_name = st.text_input("Patient Name")

col1, col2 = st.columns([3, 1])
with col1:
    doctor_name = st.text_input("Doctor Name")
with col2:
    age = st.number_input("Age", min_value=1, max_value=120, step=1, value=25)

col3, col4 = st.columns(2)
with col3:
    from_date = st.date_input("From Date")
with col4:
    to_date = st.date_input("To Date")

# ── Logo (optional) ──────────────────────────────────────────────────────────
with st.expander("➕ Add Hospital Logo (optional)"):
    logo_file = st.file_uploader(
        "Upload logo — appears top-right on PDF",
        type=["png", "jpg", "jpeg"]
    )

# ── Bills ─────────────────────────────────────────────────────────────────────
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
            f"Amount {i+1} (₹)", min_value=0.0, step=1.0, key=f"amt_{i}"
        )
    bills.append((bill_date.strftime("%d/%m/%Y"), amount))

total_amount = sum(amt for _, amt in bills)
st.markdown(f"### Total: ₹ {total_amount:,.0f}")

# ── Generate ──────────────────────────────────────────────────────────────────
if st.button("📄 Generate PDF", type="primary", use_container_width=True):

    if not patient_name.strip():
        st.error("Please enter the patient name.")
        st.stop()
    if not doctor_name.strip():
        st.error("Please enter the doctor name.")
        st.stop()

    logo_path = None
    if logo_file:
        ext = "." + logo_file.name.rsplit(".", 1)[-1]
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
        tmp.write(logo_file.read())
        tmp.close()
        logo_path = tmp.name

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

    st.success("✅ PDF generated!")

    # Download button — works on all devices
    st.download_button(
        label="⬇️ Download PDF",
        data=pdf_bytes,
        file_name=f"{patient_name.strip().replace(' ', '_')}_Medical_Bills.pdf",
        mime="application/pdf",
        use_container_width=True
    )

    # ── Preview ────────────────────────────────────────────────────────────
    st.subheader("Preview")

    # Convert PDF pages to images for mobile-compatible preview
    try:
        from pdf2image import convert_from_bytes
        images = convert_from_bytes(pdf_bytes, dpi=150)
        for img in images:
            st.image(img, use_container_width=True)
    except Exception:
        # Fallback: iframe for desktop browsers
        b64 = base64.b64encode(pdf_bytes).decode("utf-8")
        st.markdown(
            f'<iframe src="data:application/pdf;base64,{b64}" '
            f'width="100%" height="700px" style="border:1px solid #ddd;border-radius:6px;"></iframe>',
            unsafe_allow_html=True
        )