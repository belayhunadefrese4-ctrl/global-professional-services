import streamlit as st

# Page Configuration & Brand Styling
st.set_page_config(
    page_title="Global Professional Services Hub",
    page_icon="💼",
    layout="centered"
)

# Custom Brand Styling
st.markdown("""
    <style>
    .main-header {
        font-size: 38px;
        background: linear-gradient(90deg, #1E3A8A, #2563EB, #06B6D4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-align: center;
        padding-top: 10px;
        padding-bottom: 5px;
    }
    .sub-text {
        font-size: 17px;
        color: #374151;
        text-align: center;
        font-weight: 500;
        margin-bottom: 25px;
    }
    .free-badge {
        background-color: #DEF7EC;
        color: #03543F;
        padding: 4px 10px;
        border-radius: 5px;
        font-weight: bold;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.markdown('<p class="main-header">🌐 Global Professional Services Hub</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">Automated Audio Transcription, Translation, Proofreading & ATS CV/Cover Letter Generation</p>', unsafe_allow_html=True)

st.markdown("---")

# Sidebar Navigation
st.sidebar.header("📂 Select a Service")
service_choice = st.sidebar.selectbox(
    "Choose what you need:",
    [
        "🎙️ Audio / Video Transcription",
        "🌍 Document Translation",
        "📄 ATS CV Generation",
        "✉️ Cover Letter Generation",
        "✍️ Text Proofreading & Polishing",
        "⚙️ Admin Dashboard (Always Free)"
    ]
)

# Admin Panel Option
if service_choice == "⚙️ Admin Dashboard (Always Free)":
    st.subheader("⚙️ Platform Admin Panel")
    st.markdown('<span class="free-badge">ALWAYS FREE ADMIN ACCESS</span>', unsafe_allow_html=True)
    st.markdown("""
    Welcome to your management dashboard! Here you can monitor incoming orders, review uploaded client files, and manage processing queues.
    * **System Status:** Online & Fully Operational
    * **Active Telebirr Account:** `0916884912`
    * **Active CBE Account:** `1000296269488` (Leamare Branch)
    """)
    st.info("As platform administrator, all system actions and file downloads are 100% free.")

else:
    st.subheader(f"Service: {service_choice}")

    # Language Selection Feature (Local + Global)
    ETHIOPIAN_LANGUAGES = [
        "🇪🇹 Amharic (አማርኛ)",
        "🇪🇹 Afaan Oromoo (Oromiffa)",
        "🇪🇹 Tigrinya (ትግርኛ)",
        "🇪🇹 Somali (Soomaali)",
        "🇪🇹 Sidama (Afaan Oromoo)",
        "🇪🇹 Wolaytta",
        "🇪🇹 Gurage"
    ]

    GLOBAL_LANGUAGES = [
        "🇺🇸/🇬🇧 English (US/UK)",
        "🇸🇦 Arabic (العربية)",
        "🇫🇷 French (Français)",
        "🇨🇳 Mandarin Chinese (中文)",
        "🇪🇸 Spanish (Español)",
        "🇩🇪 German (Deutsch)",
        "🇮🇹 Italian (Italiano)"
    ]

    ALL_LANGUAGES = ["✨ Auto-Detect Language"] + ETHIOPIAN_LANGUAGES + GLOBAL_LANGUAGES

    # Service Pricing Logic
    if "Transcription" in service_choice:
        st.markdown("🎉 <span class='free-badge'>SPECIAL OFFER: First 10 Minutes FREE!</span>", unsafe_allow_html=True)
        
        # Audio Source Language Selector
        source_lang = st.selectbox("🎙️ Audio Source Language:", ALL_LANGUAGES)
        
        duration_mins = st.number_input("Enter Audio Duration (in minutes):", min_value=1, value=15)
        billable_mins = max(0, duration_mins - 10)
        total_usd = billable_mins * 0.25
        total_etb = billable_mins * 1.0
        
        if duration_mins <= 10:
            st.success("✨ FREE Tier Applied! Total Cost: $0.00 USD / 0.00 ETB")
        else:
            st.info(f"**Billed Minutes (after 10 free mins):** {billable_mins} mins | **Total Cost:** ${total_usd:.2f} USD / {total_etb:.2f} ETB")

    elif "Translation" in service_choice:
        st.markdown("🎉 <span class='free-badge'>SPECIAL OFFER: First 2 Pages FREE!</span>", unsafe_allow_html=True)
        
        # Source and Target Language Selection
        col_lang1, col_lang2 = st.columns(2)
        with col_lang1:
            source_lang = st.selectbox("📄 Translate From (Source Language):", ALL_LANGUAGES, index=0)
        with col_lang2:
            target_lang = st.selectbox("🎯 Translate To (Target Language):", ETHIOPIAN_LANGUAGES + GLOBAL_LANGUAGES, index=0)

        page_count = st.number_input("Enter Document Page Count:", min_value=1, value=3)
        billable_pages = max(0, page_count - 2)
        total_usd = billable_pages * 0.25
        total_etb = billable_pages * 1.0
        
        if page_count <= 2:
            st.success("✨ FREE Tier Applied! Total Cost: $0.00 USD / 0.00 ETB")
        else:
            st.info(f"**Billed Pages (after 2 free pages):** {billable_pages} pages | **Total Cost:** ${total_usd:.2f} USD / {total_etb:.2f} ETB")

    elif "ATS CV" in service_choice:
        cv_lang = st.selectbox("🌐 Target Resume Language:", ["🇺🇸 English (Standard)", "🇪🇹 Amharic (አማርኛ)", "🇫🇷 French (Français)", "🇸🇦 Arabic (العربية)"])
        cv_count = st.number_input("Number of CVs to generate/rewrite:", min_value=1, value=1)
        total_usd = cv_count * 2.00
        total_etb = cv_count * 10.0
        st.info(f"**Total Cost:** ${total_usd:.2f} USD / {total_etb:.2f} ETB")

    elif "Cover Letter" in service_choice:
        letter_lang = st.selectbox("🌐 Target Cover Letter Language:", ["🇺🇸 English (Standard)", "🇪🇹 Amharic (አማርኛ)", "🇫🇷 French (Français)", "🇸🇦 Arabic (العربية)"])
        letter_count = st.number_input("Number of Cover Letters to generate:", min_value=1, value=1)
        total_usd = letter_count * 1.00
        total_etb = letter_count * 5.0
        st.info(f"**Total Cost:** ${total_usd:.2f} USD / {total_etb:.2f} ETB")

    else:  # Proofreading
        proof_lang = st.selectbox("✍️ Text Language:", ALL_LANGUAGES)
        word_count = st.number_input("Enter Word Count:", min_value=100, value=500, step=100)
        blocks = (word_count // 500) + (1 if word_count % 500 > 0 else 0)
        total_usd = blocks * 0.25
        total_etb = blocks * 1.0
        st.info(f"**Estimated Total Cost:** ${total_usd:.2f} USD / {total_etb:.2f} ETB")

    st.markdown("---")

    # File Upload Section
    st.subheader("📁 Upload Your Files or Details")
    uploaded_file = st.file_uploader("Upload document, resume draft, audio, or instructions:", type=["pdf", "docx", "txt", "mp3", "wav", "mp4"])
    client_notes = st.text_area("Provide target job description, specific instructions, or formatting preferences:")

    if st.button("🚀 Submit Order Request"):
        if uploaded_file is not None or client_notes.strip() != "":
            st.success("Details uploaded successfully! Please proceed to payment below if applicable.")
        else:
            st.warning("Please upload a file or enter instructions before submitting your order.")

    st.markdown("---")

    # Payment Gateway Section
    st.subheader("💳 Secure Payment Options")
    st.markdown("Choose your preferred payment channel below to finalize your service order.")

    tab1, tab2 = st.tabs(["🌍 International Payer Options", "🏠 Local Ethiopian Payment (Telebirr & CBE)"])

    with tab1:
        st.markdown("### International Payer Channels")
        st.markdown("""
        * **Payoneer USD Receiving Account:** *(Pending compliance review activation)*
        * **Alternative Remittance Services:** Send funds directly via **Remitly**, **Wave**, or **WorldRemit** to local CBE bank details or mobile.
        * **Account Name:** Belayhun Adefrese Metaferia
        """)

    with tab2:
        st.markdown("### Local Bank & Mobile Transfer")
        st.markdown("""
        * **📱 Telebirr:** `0916884912` (Name: Belayhun Adefrese Metaferia)
        * **🏦 Commercial Bank of Ethiopia (CBE):** 
          * **Account Number:** `1000296269488`
          * **Branch Name:** Leamare Branch (Lem Hotel Area, Addis Ababa)
          * **Account Holder:** Belayhun Adefrese Metaferia
        """)
        st.text_input("Paste Transaction Reference Code (Receipt Code):")
        st.file_uploader("Upload payment receipt screenshot:", type=["jpg", "png", "jpeg"], key="receipt_upload")

    if st.button("✅ Confirm Payment & Queue Processing"):
        st.balloons()
        st.success
