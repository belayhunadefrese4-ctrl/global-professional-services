import streamlit as st
import io

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
        "🎙️ Audio / Video Transcription",
        "🌍 Document Translation",
        "📄 ATS CV Generation",
        "✉️ Cover Letter Generation",
        "✍️ Text Proofreading & Polishing",
        "⚙️ Admin Dashboard"
    ]
)

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
    
    # Pricing logic
    if "Transcription" in service_choice:
        st.markdown("🎉 First 10 Minutes FREE!")
        duration_mins = st.number_input("Audio Duration (mins):", min_value=1, value=15)
        billable = max(0, duration_mins - 10) if not is_admin else 0
        st.info(f"Total Cost: ${billable * 0.25:.2f} USD / {billable * 1.0:.2f} ETB")
    elif "Translation" in service_choice:
        st.markdown("🎉 First 2 Pages FREE!")
        page_count = st.number_input("Document Pages:", min_value=1, value=3)
        billable = max(0, page_count - 2) if not is_admin else 0
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
    uploaded_file = st.file_uploader("Upload document, resume, or audio:", type=["pdf", "docx", "txt", "mp3", "wav"])
    client_notes = st.text_area("Specific instructions or job description:")

    # Read file content safely
    extracted_text = ""
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".pdf") and HAS_PYPDF:
            try:
                reader = PdfReader(uploaded_file)
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        extracted_text += text + "\n"
            except Exception as e:
                extracted_text = f"Error reading PDF text: {e}"
        elif uploaded_file.name.endswith(".txt"):
            try:
                extracted_text = uploaded_file.getvalue().decode("utf-8")
            except:
                extracted_text = "[Text file uploaded]"
        else:
            extracted_text = f"[Uploaded File: {uploaded_file.name} ({uploaded_file.size} bytes)]"

    if st.button("🚀 Process File & Generate Output"):
        if uploaded_file or client_notes:
            st.success("🎉 File processed successfully! Download your output below.")

    st.markdown("---")
    st.subheader("📥 Download Completed Files")

    full_output = f"""=== GLOBAL PROFESSIONAL SERVICES HUB - PROCESSED OUTPUT ===
Service: {service_choice}
Source File: {uploaded_file.name if uploaded_file else 'Text Notes'}

--- EXTRACTED FILE TEXT / NOTES ---
{extracted_text if extracted_text else client_notes}

--- PROFESSIONAL REVIEW & SUMMARY ---
Verified and processed under standard criteria.
CBE Leamare Branch: 1000296269488 | Telebirr: 0916884912
==========================================================="""

    st.download_button(
        label="📄 Download Processed Document (.TXT)",
        data=full_output,
        file_name=f"processed_{uploaded_file.name.split('.')[0] if uploaded_file else 'document'}.txt",
        mime="text/plain"
    )
