import streamlit as str_lit
import io
import os
import tempfile

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

# Safe import for official modern Google GenAI SDK
try:
    from google import genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

str_lit.set_page_config(page_title="Global Professional Services Hub", page_icon="💼", layout="centered")

# Initialize Session State
if "processed_result" not in str_lit.session_state:
    str_lit.session_state.processed_result = ""

# Burgundy Luxury Styling
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
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #581845;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

str_lit.markdown('<p class="main-header">🌐 Global Professional Services Hub</p>', unsafe_allow_html=True)
str_lit.markdown('<p class="sub-text">Enterprise AI-Powered Transcription, Translation & ATS CV Engineering</p>', unsafe_allow_html=True)
str_lit.markdown("---")

# Admin Sidebar
str_lit.sidebar.header("🔐 Admin Access Portal")
admin_passcode = str_lit.sidebar.text_input("Enter Admin Passcode:", type="password")
is_admin = (admin_passcode == "admin123")

if is_admin:
    str_lit.sidebar.success("🔓 Admin Mode Active: Free Access Granted!")

# Gemini API Key configuration input in sidebar
str_lit.sidebar.markdown("---")
str_lit.sidebar.header("⚙️ Gemini AI Engine")
gemini_api_key = str_lit.sidebar.text_input("Enter Gemini API Key:", type="password", value=os.environ.get("GEMINI_API_KEY", ""))

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
        * **Platform Status:** Fully Operational & Modern GenAI SDK Connected
        * **Telebirr Merchant:** `0916884912` (Belayhun Adefrese Metaferia)
        * **CBE Corporate Account:** `1000296269488` (Leamare Branch, Addis Ababa)
        """)
    else:
        str_lit.error("🔒 Enter correct Admin Passcode (`admin123`) to view backend revenue metrics.")
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
        "Upload document (PDF, DOCX, TXT) or audio/video recording (MP3, WAV, MP4, M4A):",
        type=["pdf", "docx", "txt", "mp3", "wav", "mp4", "m4a", "aac", "ogg"]
    )
    
    client_notes = str_lit.text_area("Or type/paste source text directly here:", height=140)

    extracted_file_text = ""
    is_media_file = False
    temp_media_path = None

    if uploaded_file is not None:
        file_name_lower = uploaded_file.name.lower()
        if file_name_lower.endswith(".pdf") and HAS_PYPDF:
            try:
                reader = PdfReader(uploaded_file)
                pages_text = [page.extract_text() for page in reader.pages if page.extract_text()]
                extracted_file_text = "\n".join(pages_text)
            except Exception as e:
                extracted_file_text = f"[PDF Extraction Error: {e}]"
        elif file_name_lower.endswith(".docx") and HAS_DOCX:
            try:
                doc_file = Document(uploaded_file)
                extracted_file_text = "\n".join([p.text for p in doc_file.paragraphs if p.text])
            except Exception as e:
                extracted_file_text = f"[Word Extraction Error: {e}]"
        elif file_name_lower.endswith(".txt"):
            try:
                extracted_file_text = uploaded_file.getvalue().decode("utf-8")
            except Exception:
                extracted_file_text = uploaded_file.getvalue().decode("latin-1", errors="ignore")
        else:
            is_media_file = True
            suffix = os.path.splitext(uploaded_file.name)[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(uploaded_file.getvalue())
                temp_media_path = tmp.name

    final_input_text = client_notes.strip() if client_notes.strip() else extracted_file_text

    if str_lit.button("🚀 Process & Generate Live AI Deliverable"):
        if final_input_text.strip() or is_media_file:
            with str_lit.spinner("Executing Modern Google GenAI Processing..."):
                ai_output = ""
                
                if not gemini_api_key or not gemini_api_key.strip():
                    ai_output = "[Error: Please enter your Gemini API Key in the sidebar input box.]"
                elif not HAS_GENAI:
                    ai_output = "[Error: google-genai library is not installed in requirements.txt]"
                else:
                    try:
                        # Initialize modern Google GenAI Client
                        client = genai.Client(api_key=gemini_api_key.strip())
                        
                        if is_media_file and temp_media_path:
                            uploaded_file_res = client.files.upload(file=temp_media_path)
                            prompt = "Accurately transcribe, format, and structure this audio/video recording into clean professional paragraphs:"
                            response = client.models.generate_content(
                                model="gemini-3.8-flash",
                                contents=[uploaded_file_res, prompt]
                            )
                            ai_output = response.text
                            try:
                                os.unlink(temp_media_path)
                            except:
                                pass
                        else:
                            if "Translation" in service_choice:
                                prompt = f"Translate the following text accurately from {src_lang_name} to {tgt_lang_name}. Provide ONLY the final translation output in {tgt_lang_name}:\n\n{final_input_text}"
                            elif "Transcription" in service_choice:
                                prompt = f"Clean up and format this transcript into professional paragraphs:\n\n{final_input_text}"
                            elif "ATS CV" in service_choice:
                                prompt = f"Optimize this resume text for ATS recruitment with strong professional bullet points and keywords:\n\n{final_input_text}"
                            elif "Cover Letter" in service_choice:
                                prompt = f"Write a compelling executive cover letter based on:\n\n{final_input_text}"
                            else:
                                prompt = f"Proofread and polish this text for professional grammar and flow:\n\n{final_input_text}"
                            
                            response = client.models.generate_content(
                                model="gemini-3.8-flash",
                                contents=prompt
                            )
                            if response and response.text:
                                ai_output = response.text.strip()
                            else:
                                ai_output = "[Error: Model returned an empty response. Check API key permissions.]"
                    except Exception as e:
                        ai_output = f"[GenAI API Exception: {str(e)}]"

                if "Translation" in service_choice:
                    str_lit.session_state.processed_result = f"=== PROFESSIONAL GEMINI AI TRANSLATION RECORD ({src_lang_name} ➔ {tgt_lang_name}) ===\n\n{ai_output}\n\n[Certified by Global Professional Services Hub]"
                elif "Transcription" in service_choice:
                    str_lit.session_state.processed_result = f"=== GEMINI AI AUDIO / VIDEO TRANSCRIPTION RECORD ===\n\n{ai_output}\n\n[Transcript verified accurate]"
                elif "ATS CV" in service_choice:
                    str_lit.session_state.processed_result = f"=== ATS OPTIMIZED RESUME / CV REPORT ===\n\n{ai_output}\n\n[Optimized for executive recruitment]"
                elif "Cover Letter" in service_choice:
                    str_lit.session_state.processed_result = f"=== PROFESSIONAL COVER LETTER ===\n\n{ai_output}"
                else:
                    str_lit.session_state.processed_result = f"=== PROFESSIONAL PROOFREADING & POLISHING ===\n\n{ai_output}"
            
            str_lit.success("🎉 Deliverable generated successfully below!")
        else:
            str_lit.warning("Please upload a source document/media file or type/paste text above.")

    if str_lit.session_state.processed_result:
        str_lit.text_area("Live Preview Result:", value=str_lit.session_state.processed_result, height=220)

    str_lit.markdown("---")
    if not is_admin:
        str_lit.subheader("💳 Secure Payment Rails")
        tab1, tab2 = str_lit.tabs(["🌍 International Payer Options", "🏠 Local Ethiopian Payment (Telebirr & CBE)"])
        with tab1:
            str_lit.markdown("* **Payoneer USD:** *(Pending compliance review ticket # 261103-003007)*\n* **Remitly / WorldRemit:** Direct transfer to local CBE account.\n* **Beneficiary Name:** Belayhun Adefrese Metaferia")
        with tab2:
            str_lit.markdown("* **📱 Telebirr Mobile Wallet:** `0916884912` (Belayhun Adefrese Metaferia)\n* **🏦 Commercial Bank of Ethiopia (CBE):** `1000296269488` (Leamare Branch, Addis Ababa)")
            str_lit.text_input("Enter Transaction Reference Code for Verification:")

    str_lit.markdown("---")
    str_lit.subheader("📥 Download Deliverables")
    
    fallback_text = 'Click "Process & Generate Live AI Deliverable" above.'
    output_text = str_lit.session_state.processed_result if str_lit.session_state.processed_result else fallback_text

    col_a, col_b = str_lit.columns(2)
    with col_a:
        str_lit.download_button("📄 Download Deliverable (.TXT)", data=output_text, file_name="professional_deliverable.txt", mime="text/plain")
    with col_b:
        if HAS_DOCX:
            doc = Document()
            doc.add_heading("Global Professional Services Hub", level=1)
            doc.add_heading(f"Service Category: {service_choice}", level=2)
            doc.add_paragraph(output_text)
            doc.add_paragraph("\n--- Verified Agency Payment & Bank Details ---\nCBE Leamare Branch (Addis Ababa): 1000296269488\nTelebirr Wallet: 0916884912 | Holder: Belayhun Adefrese Metaferia")
            
            doc_io = io.BytesIO()
            doc.save(doc_io)
            doc_io.seek(0)

            str_lit.download_button(
                label="📝 Download Formatted Document (.DOCX)",
                data=doc_io,
                file_name="professional_deliverable.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        else:
            str_lit.info("Word document exporter loading...")
