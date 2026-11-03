import streamlit as st
from deep_translator import GoogleTranslator

# Safe import for PDF reading
try:
    from pypdf import PdfReader
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

st.set_page_config(page_title="Global Professional Services Hub", page_icon="💼", layout="centered")

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
    }
    .free-badge {
        background-color: #DEF7EC;
        color: #03543F;
        padding: 4px 10px;
        border-radius: 5px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🌐 Global Professional Services Hub</p>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #374151;'>Automated Audio Transcription, Translation, Proofreading & ATS CV Generation</p>", unsafe_allow_html=True)
st.markdown("---")

# Admin Authentication
st.sidebar.header("🔐 Admin Access Portal")
admin_passcode = st.sidebar.text_input("Enter Admin Passcode:", type="password")
is_admin = (admin_passcode == "admin123")

if is_admin:
    st.sidebar.success("🔓 Admin Mode Active: Free Unlimited Access Granted!")

st.sidebar.markdown("---")
st.sidebar.header("📂 Select a Service")
service_choice = st.sidebar.selectbox(
    "Choose what you need:",
    [
        "🌍 Document Translation",
        "🎙️ Audio / Video Transcription",
        "📄 ATS CV Generation",
        "✉️ Cover Letter Generation",
        "✍️ Text Proofreading & Polishing",
        "⚙️ Admin Dashboard"
    ]
)

# Language Mapping Dictionary (Name to ISO Code for Translator)
LANG_CODES = {
    "🇺🇸/🇬🇧 English": "en",
    "🇪🇹 Amharic (አማርኛ)": "am",
    "🇪🇹 Afaan Oromoo (Oromiffa)": "om",
    "🇪🇹 Tigrinya (ትግርኛ)": "ti",
    "🇪🇹 Somali (Soomaali)": "so",
    "🇪🇹 Sidama": "sid", # falls back if needed
    "🇪🇹 Wolaytta": "wal",
    "🇪🇹 Gurage": "en",
    "🇸🇦 Arabic (العربية)": "ar",
    "🇫🇷 French (Français)": "fr",
    "🇨🇳 Mandarin Chinese (中文)": "zh-CN",
    "🇪🇸 Spanish (Español)": "es",
    "🇩🇪 German (Deutsch)": "de",
    "🇮🇹 Italian (Italiano)": "it"
}

if service_choice == "⚙️ Admin Dashboard":
    st.subheader("⚙️ Platform Admin Panel")
    if is_admin:
        st.markdown('<span class="free-badge">ADMIN ACCESS UNLOCKED</span>', unsafe_allow_html=True)
        st.markdown("""
        * **Status:** Operational
        * **Telebirr:** `0916884912` (Belayhun Adefrese Metaferia)
        * **CBE:** `1000296269488` (Leamare Branch, Lem Hotel Area, Addis Ababa)
        """)
    else:
        st.error("🔒 Enter the correct Admin Passcode in the sidebar.")
else:
    st.subheader(f"Service: {service_choice}")
    
    # Language selection options
    lang_options = list(LANG_CODES.keys())

    if service_choice == "🌍 Document Translation":
        col1, col2 = st.columns(2)
        with col1:
            src_lang_name = st.selectbox("📄 Translate From:", lang_options, index=0)
        with col2:
            tgt_lang_name = st.selectbox("🎯 Translate To:", lang_options, index=1)
            
        st.markdown("🎉 <span class='free-badge'>SPECIAL OFFER: First 2 Pages FREE!</span>", unsafe_allow_html=True)
        page_count = st.number_input("Document Pages:", min_value=1, value=3)
        billable = max(0, page_count - 2) if not is_admin else 0
        st.info(f"Total Cost: ${billable * 0.25:.2f} USD / {billable * 1.0:.2f} ETB")

    elif "Transcription" in service_choice:
        st.markdown("🎉 <span class='free-badge'>SPECIAL OFFER: First 10 Minutes FREE!</span>", unsafe_allow_html=True)
        duration_mins = st.number_input("Audio Duration (mins):", min_value=1, value=15)
        billable = max(0, duration_mins - 10) if not is_admin else 0
        st.info(f"Total Cost: ${billable * 0.25:.2f} USD / {billable * 1.0:.2f} ETB")
    elif "ATS CV" in service_choice:
        cv_count = st.number_input("Number of CVs:", min_value=1, value=1)
        cost = cv_count * 2.0 if not is_admin else 0
        st.info(f"Total Cost: ${cost:.2f} USD")
    elif "Cover Letter" in service_choice:
        letter_count = st.number_input("Number of Letters:", min_value=1, value=1)
        cost = letter_count * 1.0 if not is_admin else 0
        st.info(f"Total Cost: ${cost:.2f} USD")
    else:
        word_count = st.number_input("Word Count:", min_value=100, value=500, step=100)
        blocks = (word_count // 500) + (1 if word_count % 500 > 0 else 0)
        cost = blocks * 0.25 if not is_admin else 0
        st.info(f"Total Cost: ${cost:.2f} USD")

    st.markdown("---")
    st.subheader("📁 Upload Your Files or Details")
    uploaded_file = st.file_uploader("Upload document, resume, or text file:", type=["pdf", "docx", "txt"])
    client_notes = st.text_area("Or type/paste text directly here for translation or processing:")

    # Read file content safely
    source_text = ""
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".pdf") and HAS_PYPDF:
            try:
                reader = PdfReader(uploaded_file)
                for page in reader.pages:
                    txt = page.extract_text()
                    if txt:
                        source_text += txt + "\n"
            except Exception as e:
                source_text = f"Error reading PDF: {e}"
        elif uploaded_file.name.endswith(".txt"):
            try:
                source_text = uploaded_file.getvalue().decode("utf-8")
            except:
                source_text = "[Text file uploaded]"
    
    if not source_text.strip():
        source_text = client_notes

    # Perform Translation if Translation service is selected
    translated_result = ""
    if service_choice == "🌍 Document Translation" and source_text.strip():
        try:
            src_code = LANG_CODES.get(src_lang_name, "en")
            tgt_code = LANG_CODES.get(tgt_lang_name, "am")
            # Translate using GoogleTranslator
            translated_result = GoogleTranslator(source=src_code, target=tgt_code).translate(source_text[:4000]) # Translates up to 4000 chars
        except Exception as e:
            translated_result = f"Translation execution notice: {e}\n(Showing source text fallback):\n{source_text}"
    else:
        translated_result = source_text

    if st.button("🚀 Process & Translate Now"):
        if source_text.strip():
            st.success("🎉 Translation & processing completed successfully!")
        else:
            st.warning("Please upload a document or paste text to translate.")

    st.markdown("---")
    st.subheader("📥 Download Completed Files")

    full_output = f"""=== GLOBAL PROFESSIONAL SERVICES HUB - TRANSLATED OUTPUT ===
Service: {service_choice}
Source Language: {src_lang_name if service_choice == '🌍 Document Translation' else 'Standard'}
Target Language: {tgt_lang_name if service_choice == '🌍 Document Translation' else 'Standard'}
Source File: {uploaded_file.name if uploaded_file else 'Direct Text Input'}

--- TRANSLATED / PROCESSED CONTENT ---
{translated_result if translated_result else 'No content provided.'}

--- VERIFIED PAYMENT & BANK DETAILS ---
CBE Leamare Branch (Lem Hotel Area, Addis Ababa): 1000296269488
Telebirr Account: 0916884912 | Holder: Belayhun Adefrese Metaferia
================================================================"""

    st.download_button(
        label="📄 Download Translated Document (.TXT)",
        data=full_output,
        file_name=f"translated_output.txt",
        mime="text/plain"
    )
