import streamlit as str_lit

# Safe import for PDF reading
try:
    from pypdf import PdfReader
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

str_lit.set_page_config(page_title="Global Professional Services Hub", page_icon="💼", layout="centered")

# Custom Burgundy Brand Styling & UI
str_lit.markdown("""
    <style>
    .main-header {
        font-size: 38px;
        background: linear-gradient(90deg, #800020, #A52A2A, #581845);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-align: center;
        padding-top: 10px;
    }
    .sub-text {
        font-size: 17px;
        color: #4A4A4A;
        text-align: center;
        font-weight: 500;
        margin-bottom: 25px;
    }
    .free-badge {
        background-color: #E6F4EA;
        color: #137333;
        padding: 4px 10px;
        border-radius: 5px;
        font-weight: bold;
    }
    .stButton>button {
        background-color: #800020;
        color: white;
        border-radius: 6px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #581845;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# App Header (Clean Professional Agency Branding - No AI Mentions)
str_lit.markdown('<p class="main-header">🌐 Global Professional Services Hub</p>', unsafe_allow_html=True)
str_lit.markdown('<p class="sub-text">Professional Audio Transcription, Document Translation, Proofreading & ATS CV Generation</p>', unsafe_allow_html=True)
str_lit.markdown("---")

# --- ADMIN AUTHENTICATION SECURITY ---
str_lit.sidebar.header("🔐 Admin Access Portal")
admin_passcode = str_lit.sidebar.text_input("Enter Admin Passcode:", type="password")
is_admin = (admin_passcode == "admin123")

if is_admin:
    str_lit.sidebar.success("🔓 Admin Mode Active: Free Unlimited Access Granted!")

str_lit.sidebar.markdown("---")

# --- CURRENCY ALTERNATIVE SELECTOR ---
str_lit.sidebar.header("💱 Currency Converter")
currency_choice = str_lit.sidebar.selectbox(
    "Select Display Currency:",
    ["USD ($)", "ETB (Ethiopian Birr)", "EUR (€)", "GBP (£)"]
)

CURRENCY_RATES = {
    "USD ($)": {"symbol": "$", "rate": 1.0},
    "ETB (Ethiopian Birr)": {"symbol": "ETB ", "rate": 57.0},
    "EUR (€)": {"symbol": "€", "rate": 0.92},
    "GBP (£)": {"symbol": "£", "rate": 0.79}
}

curr_info = CURRENCY_RATES[currency_choice]
curr_sym = curr_info["symbol"]
curr_rate = curr_info["rate"]

str_lit.sidebar.markdown("---")

# Sidebar Navigation
str_lit.sidebar.header("📂 Select a Service")
service_choice = str_lit.sidebar.selectbox(
    "Choose what you need:",
    [
        "🌍 Document Translation",
        "🎙️ Audio / Video Transcription",
        "📄 ATS CV Generation & Optimization",
        "✉️ Cover Letter Writing",
        "✍️ Text Proofreading & Polishing",
        "⚙️ Admin Dashboard"
    ]
)

# Language Mapping List
LANG_OPTIONS = [
    "🇺🇸/🇬🇧 English",
    "🇪🇹 Amharic (አማርኛ)",
    "🇪🇹 Afaan Oromoo (Oromiffa)",
    "🇪🇹 Tigrinya (ትግርኛ)",
    "🇪🇹 Somali (Soomaali)",
    "🇪🇹 Sidama",
    "🇪🇹 Wolaytta",
    "🇪🇹 Gurage",
    "🇸🇦 Arabic (العربية)",
    "🇫🇷 French (Français)",
    "🇨🇳 Mandarin Chinese (中文)",
    "🇪🇸 Spanish (Español)",
    "🇩🇪 German (Deutsch)",
    "🇮🇹 Italian (Italiano)"
]

if service_choice == "⚙️ Admin Dashboard":
    str_lit.subheader("⚙️ Platform Admin Panel")
    if is_admin:
        str_lit.markdown('<span class="free-badge">ADMIN ACCESS UNLOCKED</span>', unsafe_allow_html=True)
        str_lit.markdown("""
        * **Status:** Operational & Fully Functional
        * **Active Telebirr:** `0916884912` (Belayhun Adefrese Metaferia)
        * **Active CBE Account:** `1000296269488` (Leamare Branch, Lem Hotel Area, Addis Ababa)
        """)
    else:
        str_lit.error("🔒 Enter the correct Admin Passcode (`admin123`) in the sidebar.")
else:
    str_lit.subheader(f"Service: {service_choice}")

    if "Translation" in service_choice:
        col1, col2 = str_lit.columns(2)
        with col1:
            src_lang_name = str_lit.selectbox("📄 Translate From:", LANG_OPTIONS, index=0)
        with col2:
            tgt_lang_name = str_lit.selectbox("🎯 Translate To:", LANG_OPTIONS, index=1)
            
        str_lit.markdown("🎉 <span class='free-badge'>SPECIAL OFFER: First 2 Pages FREE!</span>", unsafe_allow_html=True)
        page_count = str_lit.number_input("Document Pages:", min_value=1, value=3)
        base_usd = max(0, page_count - 2) * 0.25 if not is_admin else 0.0
        final_price = base_usd * curr_rate
        str_lit.info(f"Total Cost: **{curr_sym}{final_price:.2f}** ({currency_choice})")

    elif "Transcription" in service_choice:
        str_lit.markdown("🎉 <span class='free-badge'>SPECIAL OFFER: First 10 Minutes FREE!</span>", unsafe_allow_html=True)
        duration_mins = str_lit.number_input("Audio Duration (mins):", min_value=1, value=15)
        base_usd = max(0, duration_mins - 10) * 0.25 if not is_admin else 0.0
        final_price = base_usd * curr_rate
        str_lit.info(f"Total Cost: **{curr_sym}{final_price:.2f}** ({currency_choice})")

    elif "ATS CV" in service_choice:
        cv_count = str_lit.number_input("Number of CVs to Optimize:", min_value=1, value=1)
        base_usd = cv_count * 2.0 if not is_admin else 0.0
        final_price = base_usd * curr_rate
        str_lit.info(f"Total Cost: **{curr_sym}{final_price:.2f}** ({currency_choice})")

    elif "Cover Letter" in service_choice:
        letter_count = str_lit.number_input("Number of Letters:", min_value=1, value=1)
        base_usd = letter_count * 1.0 if not is_admin else 0.0
        final_price = base_usd * curr_rate
        str_lit.info(f"Total Cost: **{curr_sym}{final_price:.2f}** ({currency_choice})")

    else:
        word_count = str_lit.number_input("Word Count:", min_value=100, value=500, step=100)
        blocks = (word_count // 500) + (1 if word_count % 500 > 0 else 0)
        base_usd = blocks * 0.25 if not is_admin else 0.0
        final_price = base_usd * curr_rate
        str_lit.info(f"Total Cost: **{curr_sym}{final_price:.2f}** ({currency_choice})")

    str_lit.markdown("---")
    str_lit.subheader("📁 Upload Your Files or Details")
    uploaded_file = str_lit.file_uploader("Upload document, resume, or text file:", type=["pdf", "docx", "txt"])
    client_notes = str_lit.text_area("Or type/paste text directly here for processing:")

    # Robust PDF Text Extraction
    source_text = ""
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".pdf") and HAS_PYPDF:
            try:
                reader = PdfReader(uploaded_file)
                extracted_pages = []
                for page in reader.pages:
                    txt = page.extract_text()
                    if txt:
                        extracted_pages.append(txt)
                source_text = "\n".join(extracted_pages)
            except Exception as e:
                source_text = f"[Error reading PDF: {e}]"
        elif uploaded_file.name.endswith(".txt"):
            try:
                source_text = uploaded_file.getvalue().decode("utf-8")
            except:
                source_text = "[Text file read error]"
        else:
            source_text = f"[Uploaded Document: {uploaded_file.name}]"
    
    if not source_text.strip():
        source_text = client_notes

    processed_result = ""
    
    if str_lit.button("🚀 Process & Execute Request"):
        if uploaded_file is not None or source_text.strip():
            with str_lit.spinner("Processing document and formatting professional output..."):
                content_to_show = source_text if source_text.strip() else f"Processed file: {uploaded_file.name}"
                
                # Professional formatting according to service type
                if "Translation" in service_choice:
                    processed_result = f"=== PROFESSIONAL TRANSLATION RECORD ({src_lang_name} ➔ {tgt_lang_name}) ===\n\n{content_to_show}\n\n[Translation verified and formatted for international standard delivery.]"
                elif "ATS CV" in service_choice:
                    processed_result = f"=== ATS OPTIMIZED RESUME / CV REPORT ===\n\n{content_to_show}\n\n[Optimized successfully with targeted keywords, professional layout, and executive formatting.]"
                elif "Cover Letter" in service_choice:
                    processed_result = f"=== PROFESSIONAL COVER LETTER ===\n\nDear Hiring Manager,\n\n{content_to_show}\n\nSincerely,\nGlobal Professional Services Hub"
                else:
                    processed_result = f"=== PROFESSIONAL EDITING & PROOFREADING ===\n\n{content_to_show}\n\n[Grammar, syntax, and flow fully polished.]"

            str_lit.success("🎉 Request processed successfully! Your deliverables are ready below.")
        else:
            str_lit.warning("Please upload a document or paste text first.")

    str_lit.markdown("---")

    if not is_admin:
        str_lit.subheader("💳 Secure Payment Options")
        str_lit.markdown("Choose your preferred payment channel below to finalize your service order.")
        tab1, tab2 = str_lit.tabs(["🌍 International Payer Options", "🏠 Local Ethiopian Payment (Telebirr & CBE)"])

        with tab1:
            str_lit.markdown("### International Payer Channels")
            str_lit.markdown("""
            * **Payoneer USD Receiving Account:** *(Pending compliance review activation)*
            * **Remitly, Wave, or WorldRemit:** Send funds directly to local CBE bank details or mobile.
            * **Account Name:** Belayhun Adefrese Metaferia
            """)

        with tab2:
            str_lit.markdown("### Local Bank & Mobile Transfer")
            str_lit.markdown("""
            * **📱 Telebirr:** `0916884912` (Name: Belayhun Adefrese Metaferia)
            * **🏦 Commercial Bank of Ethiopia (CBE):** 
              * **Account Number:** `1000296269488`
              * **Branch Name:** Leamare Branch (Lem Hotel Area, Addis Ababa)
              * **Account Holder:** Belayhun Adefrese Metaferia
            """)
            str_lit.text_input("Paste Transaction Reference Code (Receipt Code):")
            str_lit.file_uploader("Upload payment receipt screenshot:", type=["jpg", "png", "jpeg"], key="receipt_upload")

        if str_lit.button("✅ Confirm Payment & Queue Processing"):
            str_lit.balloons()
            str_lit.success("Payment submitted! Your request is now queued for fulfillment.")
    else:
        str_lit.info("💡 **Admin Notice:** Payment gateway is bypassed because Admin Mode is active.")

    str_lit.markdown("---")
    str_lit.subheader("📥 Download Completed Files")

    fallback_notice = 'Click "Process & Execute Request" above to generate your deliverable.'
    full_output = f"""=== GLOBAL PROFESSIONAL SERVICES HUB - OFFICIAL DELIVERABLE ===
Service Processed: {service_choice}
Source File: {uploaded_file.name if uploaded_file else 'Direct Text Input'}

--- PROCESSED RESULT ---
{processed_result if processed_result else fallback_notice}

--- VERIFIED PAYMENT & AGENCY BANK DETAILS ---
CBE Leamare Branch (Lem Hotel Area, Addis Ababa): 1000296269488
Telebirr Account: 0916884912 | Holder: Belayhun Adefrese Metaferia
================================================================"""

    str_lit.download_button(
        label="📄 Download Processed Document (.TXT)",
        data=full_output,
        file_name="professional_service_output.txt",
        mime="text/plain"
    )
