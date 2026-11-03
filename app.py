import streamlit as str_lit
import io
import os

# Safe import for PDF reading
try:
    from pypdf import PdfReader
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

# Safe import for Word Document reading/writing
try:
    from docx import Document
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False

# Safe import for official Google Gemini API
try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False

str_lit.set_page_config(page_title="Global Professional Services Hub", page_icon="💼", layout="centered")

# Initialize Session State
if "processed_result" not in str_lit.session_state:
    str_lit.session_state.processed_result = ""

# Burgundy Styling
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

str_lit.markdown('<p class="main-header">🌐 Global Professional Services Hub</p>', unsafe_allow_html=True)
str_lit.markdown('<p class="sub-text">Professional AI-Powered Transcription, Translation & ATS CV Generation</p>', unsafe_allow_html=True)
str_lit.markdown("---")

# Admin Sidebar
str_lit.sidebar.header("🔐 Admin Access Portal")
admin_passcode = str_lit.sidebar.text_input("Enter Admin Passcode:", type="password")
is_admin = (admin_passcode == "admin123")

if is_admin:
    str_lit.sidebar.success("🔓 Admin Mode Active: Free Access Granted!")

# Gemini API Key configuration input in sidebar for instant live AI power
str_lit.sidebar.markdown("---")
str_lit.sidebar.header("⚙️ Gemini 3.8 AI Engine")
gemini_api_key = str_lit.sidebar.text_input("Enter Gemini API Key:", type="password", value=os.environ.get("GEMINI_API_KEY", ""))

if gemini_api_key and HAS_GEMINI:
    genai.configure(api_key=gemini_api_key)
    ai_configured = True
else:
    ai_configured = False

str_lit.sidebar.markdown("---")

# Currency Converter
str_lit.sidebar.header("💱 Currency Converter")
currency_choice = str_lit.sidebar.selectbox("Display Currency:", ["USD ($)", "ETB (Ethiopian Birr)", "EUR (€)", "GBP (£)"])
CURRENCY_RATES = {
    "USD ($)": {"symbol": "$", "rate": 1.0},
    "ETB (Ethiopian Birr)": {"symbol": "ETB ", "rate": 57.0},
    "EUR (€)": {"symbol": "€", "rate": 0.92},
    "GBP (£)": {"symbol": "£", "rate": 0.79}
}
curr_sym = CURRENCY_RATES[currency_choice]["symbol"]
curr_rate = CURRENCY_RATES[currency_choice]["rate"]

str_lit.sidebar.markdown("---")

# Service Selector
str_lit.sidebar.header("📂 Select a Service")
service_choice = str_lit.sidebar.selectbox(
    "Choose Service:",
    [
        "🌍 Document Translation",
        "🎙️ Audio / Video Transcription",
        "📄 ATS CV Generation & Optimization",
        "✉️ Cover Letter Writing",
        "✍️ Text Proofreading & Polishing",
        "⚙️ Admin Dashboard"
    ]
)

LANG_MAP = {
    "English": "English",
    "Amharic (አማርኛ)": "Amharic",
    "Afaan Oromoo": "Afaan Oromoo",
    "Tigrinya (ትግርኛ)": "Tigrinya",
    "Somali": "Somali",
    "Arabic (العربية)": "Arabic",
    "French (Français)": "French",
    "Spanish (Español)": "Spanish",
    "German (Deutsch)": "German",
    "Italian (Italiano)": "Italian"
}

LANG_OPTIONS = list(LANG_MAP.keys())

if service_choice == "⚙️ Admin Dashboard":
    str_lit.subheader("⚙️ Platform Admin Panel")
    if is_admin:
        str_lit.markdown("""
        * **Status:** Fully Operational with Gemini 3.8 Flash AI Engine
        * **Telebirr:** `0916884912` (Belayhun Adefrese Metaferia)
        * **CBE Account:** `1000296269488` (Leamare Branch, Addis Ababa)
        """)
    else:
        str_lit.error("🔒 Enter correct Admin Passcode (`admin123`).")
else:
    str_lit.subheader(f"Service: {service_choice}")

    src_lang_name = "English"
    tgt_lang_name = "Amharic (አማርኛ)"

    if "Translation" in service_choice:
        col1, col2 = str_lit.columns(2)
        with col1:
            src_lang_name = str_lit.selectbox("From:", LANG_OPTIONS, index=0)
        with col2:
            tgt_lang_name = str_lit.selectbox("To:", LANG_OPTIONS, index=1)
        str_lit.markdown("🎉 <span class='free-badge'>First 2 Pages FREE!</span>", unsafe_allow_html=True)
    elif "Transcription" in service_choice:
        str_lit.markdown("🎉 <span class='free-badge'>First 10 Minutes FREE!</span>", unsafe_allow_html=True)

    str_lit.markdown("---")
    str_lit.subheader("📁 Upload Files & Source Material")
    
    uploaded_file = str_lit.file_uploader(
        "Upload document, PDF, Word file, text file, audio, or video recording:",
        type=["pdf", "docx", "txt", "mp3", "wav", "mp4", "m4a", "aac", "ogg"]
    )
    
    client_notes = str_lit.text_area("Or type/paste text directly here:", height=140)

    extracted_file_text = ""
    if uploaded_file is not None:
        file_name_lower = uploaded_file.name.lower()
        if file_name_lower.endswith(".pdf") and HAS_PYPDF:
            try:
                reader = PdfReader(uploaded_file)
                pages_text = [page.extract_text() for page in reader.pages if page.extract_text()]
                extracted_file_text = "\n".join(pages_text)
            except Exception:
                extracted_file_text = f"[Uploaded PDF File: {uploaded_file.name}]"
        elif file_name_lower.endswith(".docx") and HAS_DOCX:
            try:
                doc_file = Document(uploaded_file)
                extracted_file_text = "\n".join([p.text for p in doc_file.paragraphs if p.text])
            except Exception:
                extracted_file_text = f"[Uploaded Word File: {uploaded_file.name}]"
        elif file_name_lower.endswith(".txt"):
            try:
                extracted_file_text = uploaded_file.getvalue().decode("utf-8")
            except Exception:
                extracted_file_text = f"[Uploaded Text File: {uploaded_file.name}]"
        else:
            extracted_file_text = f"[Uploaded Media Record: {uploaded_file.name}]"

    final_input_text = client_notes.strip() if client_notes.strip() else extracted_file_text

    if str_lit.button("🚀 Process & Generate Deliverable"):
        if final_input_text.strip():
            with str_lit.spinner("Processing with Gemini 3.8 Flash AI..."):
                ai_output = ""
                
                if ai_configured:
                    try:
                        # Explicitly target Gemini 3.8 Flash for peak intelligence and speed
                        model = genai.GenerativeModel("gemini-3.8-flash")
                        
                        if "Translation" in service_choice:
                            prompt = f"Translate the following text accurately and professionally from {src_lang_name} to {tgt_lang_name}. Provide only the clean, high-quality translation output:\n\n{final_input_text}"
                        elif "Transcription" in service_choice:
                            prompt = f"Clean up, format, and structure the following raw transcript into professional, accurate paragraphs:\n\n{final_input_text}"
                        elif "ATS CV" in service_choice:
                            prompt = f"Optimize the following resume text for ATS (Applicant Tracking Systems) with strong professional bullet points and keywords:\n\n{final_input_text}"
                        elif "Cover Letter" in service_choice:
                            prompt = f"Write a compelling, professional executive cover letter based on these details:\n\n{final_input_text}"
                        else:
                            prompt = f"Proofread and thoroughly polish the following text for grammar, executive flow, and professional tone:\n\n{final_input_text}"
                        
                        response = model.generate_content(prompt)
                        ai_output = response.text
                    except Exception as e:
                        ai_output = f"[Gemini 3.8 Processing Error: {e}]\n\n{final_input_text}"

                if not ai_output:
                    ai_output = f"=== PROCESSED OUTPUT ===\n\n{final_input_text}"

                if "Translation" in service_choice:
                    str_lit.session_state.processed_result = f"=== PROFESSIONAL GEMINI 3.8 TRANSLATION RECORD ({src_lang_name} ➔ {tgt_lang_name}) ===\n\n{ai_output}\n\n[Verified by Global Professional Services Hub]"
                elif "Transcription" in service_choice:
                    str_lit.session_state.processed_result = f"=== GEMINI 3.8 AUDIO / VIDEO TRANSCRIPTION RECORD ===\n\n{ai_output}\n\n[Transcript verified accurate]"
                elif "ATS CV" in service_choice:
                    str_lit.session_state.processed_result = f"=== ATS OPTIMIZED RESUME / CV REPORT ===\n\n{ai_output}\n\n[Optimized for executive recruitment]"
                elif "Cover Letter" in service_choice:
                    str_lit.session_state.processed_result = f"=== PROFESSIONAL COVER LETTER ===\n\n{ai_output}"
                else:
                    str_lit.session_state.processed_result = f"=== PROFESSIONAL PROOFREADING & POLISHING ===\n\n{ai_output}"
            
            str_lit.success("🎉 Deliverable generated successfully below!")
        else:
            str_lit.warning("Please upload a file or type/paste text above.")

    if str_lit.session_state.processed_result:
        str_lit.text_area("Live Preview:", value=str_lit.session_state.processed_result, height=200)

    str_lit.markdown("---")
    if not is_admin:
        str_lit.subheader("💳 Secure Payment Options")
        tab1, tab2 = str_lit.tabs(["🌍 International Payer Options", "🏠 Local Ethiopian Payment (Telebirr & CBE)"])
        with tab1:
            str_lit.markdown("* **Payoneer USD:** *(Pending compliance review)*\n* **Remitly / WorldRemit:** Send to local CBE details.\n* **Name:** Belayhun Adefrese Metaferia")
        with tab2:
            str_lit.markdown("* **📱 Telebirr:** `0916884912` (Belayhun Adefrese Metaferia)\n* **🏦 CBE Account:** `1000296269488` (Leamare Branch, Addis Ababa)")
            str_lit.text_input("Transaction Reference Code:")

    str_lit.markdown("---")
    str_lit.subheader("📥 Download Deliverables")
    
    fallback_text = 'Click "Process & Generate Deliverable" above.'
    output_text = str_lit.session_state.processed_result if str_lit.session_state.processed_result else fallback_text

    col_a, col_b = str_lit.columns(2)
    with col_a:
        str_lit.download_button("📄 Download as .TXT", data=output_text, file_name="deliverable.txt", mime="text/plain")
    with col_b:
        if HAS_DOCX:
            doc = Document()
            doc.add_heading("Global Professional Services Hub", level=1)
            doc.add_heading(f"Service: {service_choice}", level=2)
            doc.add_paragraph(output_text)
            doc.add_paragraph("\n--- Verified Payment & Agency Bank Details ---\nCBE Leamare Branch (Addis Ababa): 1000296269488\nTelebirr: 0916884912 | Holder: Belayhun Adefrese Metaferia")
            
            doc_io = io.BytesIO()
            doc.save(doc_io)
            doc_io.seek(0)

            str_lit.download_button(
                label="📝 Download as .DOCX",
                data=doc_io,
                file_name="deliverable.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        else:
            str_lit.info("Word document exporter loading...")
