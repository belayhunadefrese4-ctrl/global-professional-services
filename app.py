import streamlit as st
import io
import os
import tempfile
import time

# --- DEPENDENCY SAFEE IMPORTS ---
try:
    from pypdf import PdfReader
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

try:
    from docx import Document
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False

try:
    from google import genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

st.set_page_config(page_title="Belayhun AI Global Services", page_icon="🌐", layout="wide")

# Persistent State Management
if "processed_result" not in st.session_state:
    st.session_state.processed_result = ""

# Executive Burgundy Styling
st.markdown("""
    <style>
    .main-title {
        font-size: 34px;
        background: linear-gradient(90deg, #800020, #A52A2A, #581845);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-align: center;
    }
    .stButton>button {
        background-color: #800020;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        width: 100%;
        padding: 10px;
    }
    .stButton>button:hover {
        background-color: #581845;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🌐 Belayhun AI Enterprise Hub</p>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar Configuration
st.sidebar.header("🔐 Engine & API Settings")
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password", value=os.environ.get("GEMINI_API_KEY", ""))

st.sidebar.markdown("---")
st.sidebar.header("📂 Service Selector")
service = st.sidebar.radio(
    "Select Feature:",
    [
        "🌍 Document Translation",
        "🎙️ Audio / Video Transcription",
        "📝 Text & Document Summarizer",
        "📄 ATS CV & Cover Letter Builder",
        "✍️ Proofreading & Editing",
        "⚙️ Admin Dashboard"
    ]
)

# Shared File Extraction Helper
def extract_text_from_file(uploaded_file):
    if uploaded_file is None:
        return ""
    file_name = uploaded_file.name.lower()
    if file_name.endswith(".pdf") and HAS_PYPDF:
        reader = PdfReader(uploaded_file)
        return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif file_name.endswith(".docx") and HAS_DOCX:
        doc = Document(uploaded_file)
        return "\n".join([p.text for p in doc.paragraphs if p.text])
    elif file_name.endswith(".txt"):
        return uploaded_file.getvalue().decode("utf-8", errors="ignore")
    return ""

if service == "⚙️ Admin Dashboard":
    st.subheader("⚙️ System Control & Revenue Dashboard")
    st.markdown("""
    * **Platform Engine Status:** Operational (`gemini-1.5-flash`)
    * **Telebirr Wallet:** `0986884912` (Belayhun Adefrese Metaferia)
    * **CBE Account:** `1000296269488` (Leamare Branch, Addis Ababa)
    * **Capital Market Link:** [Access Capital Market Engine](https://capital-market-engine-a72z6ry6eqo2zkjn3hh3de.streamlit.app/)
    """)
else:
    st.subheader(f"Service: {service}")

    # Specific Service Options
    target_lang = "Amharic"
    if service == "🌍 Document Translation":
        col1, col2 = st.columns(2)
        with col1:
            src_lang = st.selectbox("From:", ["English", "Amharic", "Afaan Oromoo", "Tigrinya", "French", "Arabic"])
        with col2:
            target_lang = st.selectbox("To:", ["Amharic", "English", "Afaan Oromoo", "Tigrinya", "French", "Arabic"])

    # File Input Section
    uploaded_file = st.file_uploader(
        "Upload Source File (PDF, DOCX, TXT, MP3, WAV, MP4, M4A):",
        type=["pdf", "docx", "txt", "mp3", "wav", "mp4", "m4a"]
    )
    user_prompt = st.text_area("Or type / paste source text directly here:", height=150)

    if st.button("🚀 Execute AI Service Processing"):
        if not api_key:
            st.error("Please enter a valid Gemini API Key in the sidebar.")
        elif not HAS_GENAI:
            st.error("The `google-genai` library is missing. Ensure `google-genai` is in requirements.txt.")
        else:
            with st.spinner("Processing request via Gemini 1.5 Flash..."):
                try:
                    client = genai.Client(api_key=api_key.strip())
                    output_text = ""

                    # Check if Audio/Video File Uploaded
                    is_media = uploaded_file and uploaded_file.name.lower().endswith((".mp3", ".wav", ".mp4", ".m4a"))

                    if is_media:
                        # Process Multimodal Audio/Video via API File Upload
                        suffix = os.path.splitext(uploaded_file.name)[1]
                        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                            tmp.write(uploaded_file.getvalue())
                            tmp_path = tmp.name

                        st.info("Uploading audio/video binary to Gemini API...")
                        uploaded_media = client.files.upload(file=tmp_path)
                        
                        # Wait briefly for processing
                        time.sleep(3)

                        prompt = "Accurately transcribe and format this audio/video recording into clear paragraphs:"
                        response = client.models.generate_content(
                            model="gemini-1.5-flash",
                            contents=[uploaded_media, prompt]
                        )
                        output_text = response.text
                        os.unlink(tmp_path)

                    else:
                        # Process Document or Raw Text
                        extracted_text = extract_text_from_file(uploaded_file)
                        combined_input = (user_prompt + "\n" + extracted_text).strip()

                        if not combined_input:
                            st.warning("Please provide input text or upload a document.")
                            st.stop()

                        if service == "🌍 Document Translation":
                            prompt = f"Translate the following text accurately into {target_lang}:\n\n{combined_input}"
                        elif service == "📝 Text & Document Summarizer":
                            prompt = f"Provide a clean, structured bulleted summary of the following document:\n\n{combined_input}"
                        elif service == "📄 ATS CV & Cover Letter Builder":
                            prompt = f"Generate an ATS-optimized professional resume and executive cover letter based on this input:\n\n{combined_input}"
                        elif service == "✍️ Proofreading & Editing":
                            prompt = f"Proofread, fix all grammar errors, and elevate the vocabulary of this text:\n\n{combined_input}"
                        else:
                            prompt = f"Clean up and structure this transcript:\n\n{combined_input}"

                        response = client.models.generate_content(
                            model="gemini-1.5-flash",
                            contents=prompt
                        )
                        output_text = response.text

                    st.session_state.processed_result = output_text
                    st.success("Processing Complete!")

                except Exception as e:
                    st.error(f"Execution Error: {str(e)}")

    # Display Output & Export Options
    if st.session_state.processed_result:
        st.markdown("---")
        st.subheader("📋 Generated Deliverable")
        st.text_area("Live Preview:", value=st.session_state.processed_result, height=250)

        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            st.download_button(
                "📄 Download Text File (.TXT)",
                data=st.session_state.processed_result,
                file_name="deliverable.txt",
                mime="text/plain"
            )
        with col_dl2:
            if HAS_DOCX:
                doc = Document()
                doc.add_heading("Belayhun AI Professional Deliverable", level=1)
                doc.add_paragraph(st.session_state.processed_result)
                doc_io = io.BytesIO()
                doc.save(doc_io)
                doc_io.seek(0)
                st.download_button(
                    "📝 Download Word Document (.DOCX)",
                    data=doc_io,
                    file_name="deliverable.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
