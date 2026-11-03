import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Global Professional Services Hub",
    page_icon="💼",
    layout="centered"
)

# App Header
st.title("🌐 Global Professional Services Platform")
st.markdown("""
Welcome! We provide automated **Audio/Video Transcription**, **Multilingual Translation**, **Proofreading**, and **ATS CV & Cover Letter Generation**.
""")

st.markdown("---")

# Sidebar for Service Selection
st.sidebar.header("Select a Service")
service_choice = st.sidebar.selectbox(
    "Choose what you need:",
    [
        "Audio / Video Transcription",
        "Document Translation",
        "ATS CV Generation",
        "Cover Letter Generation",
        "Text Proofreading & Polishing"
    ]
)

# Service Calculator & Pricing
st.subheader(f"Service: {service_choice}")

if service_choice == "Audio / Video Transcription":
    st.markdown("**Rate:** Minimum **$0.25 USD** (or **1 ETB**) per minute.")
    duration_mins = st.number_input("Enter Audio Duration (in minutes):", min_value=1, value=10)
    total_usd = duration_mins * 0.25
    total_etb = duration_mins * 1.0
    st.info(f"**Estimated Total Cost:** ${total_usd:.2f} USD / {total_etb:.2f} ETB")

elif service_choice == "Document Translation":
    st.markdown("**Rate:** **$0.25 USD** (or **1 ETB**) per page.")
    page_count = st.number_input("Enter Document Page Count:", min_value=1, value=2)
    total_usd = page_count * 0.25
    total_etb = page_count * 1.0
    st.info(f"**Estimated Total Cost:** ${total_usd:.2f} USD / {total_etb:.2f} ETB")

elif service_choice == "ATS CV Generation":
    st.markdown("**Rate:** Fixed Tier — Minimum **$2.00 USD** or **10 ETB** per document.")
    cv_count = st.number_input("Number of CVs to generate/rewrite:", min_value=1, value=1)
    total_usd = cv_count * 2.00
    total_etb = cv_count * 10.0
    st.info(f"**Total Cost:** ${total_usd:.2f} USD / {total_etb:.2f} ETB")

elif service_choice == "Cover Letter Generation":
    st.markdown("**Rate:** Fixed Tier — Minimum **$1.00 USD** or **5 ETB** per letter.")
    letter_count = st.number_input("Number of Cover Letters to generate:", min_value=1, value=1)
    total_usd = letter_count * 1.00
    total_etb = letter_count * 5.0
    st.info(f"**Total Cost:** ${total_usd:.2f} USD / {total_etb:.2f} ETB")

else:  # Proofreading
    st.markdown("**Rate:** **$0.25 USD** (or **1 ETB**) per 500 words.")
    word_count = st.number_input("Enter Word Count:", min_value=100, value=500, step=100)
    blocks = (word_count // 500) + (1 if word_count % 500 > 0 else 0)
    total_usd = blocks * 0.25
    total_etb = blocks * 1.0
    st.info(f"**Estimated Total Cost:** ${total_usd:.2f} USD / {total_etb:.2f} ETB")

st.markdown("---")

# File Upload Section
st.subheader("📁 Upload Your Files or Details")
uploaded_file = st.file_uploader("Upload document, resume draft, or job description:", type=["pdf", "docx", "txt", "mp3", "wav", "mp4"])
client_notes = st.text_area("Provide target job description, specific instructions, or target language:")

if st.button("Submit Order"):
    if uploaded_file is not None or client_notes.strip() != "":
        st.success("Details uploaded successfully! Please proceed to payment below to initiate processing.")
    else:
        st.warning("Please upload a file or enter instructions before submitting your order.")

st.markdown("---")

# Payment Section
st.subheader("💳 Payment Gateway")
st.markdown("Choose your payment method below to complete your order.")

tab1, tab2 = st.tabs(["🌍 International Payment (Payoneer)", "🏠 Local Payment (Telebirr & CBE)"])

with tab1:
    st.markdown("### Payoneer USD Receiving Account")
    st.markdown("""
    * **Bank Name:** First Century Bank / Community Federal Savings Bank
    * **Routing Number (ABA):** *(Pending Payoneer review approval)*
    * **Account Number:** *(Pending Payoneer review approval)*
    * **Account Holder:** Belayhun Adefrese Metaferia
    """)

with tab2:
    st.markdown("### Local Ethiopian Transfer")
    st.markdown("""
    * **Telebirr:** `0916884912` (Name: Belayhun Adefrese Metaferia)
    * **Commercial Bank of Ethiopia (CBE):** *[Your CBE Account Number]*
    """)
    st.text_input("Paste Telebirr / CBE Transaction Reference Code:")
    st.file_uploader("Upload screenshot receipt:", type=["jpg", "png", "jpeg"], key="receipt_upload")

if st.button("Confirm Payment & Process Request"):
    st.balloons()
    st.success("Payment details submitted! Your order is queued for processing.")
