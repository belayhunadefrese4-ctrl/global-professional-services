import streamlit as st
import os

# Safe imports for AI and PDF parsing
try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

try:
    from pypdf import PdfReader
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

# Page Configuration & Premium Branding
st.set_page_config(
    page_title="Global Professional Services Hub",
    page_icon="🌐",
    layout="centered"
)

# High-End Professional Branding & Styling (Obsidian, Navy & Gold Palette)
st.markdown("""
    <style>
    .main-header {
        font-size: 40px;
        background: linear-gradient(135deg, #0F172A, #1E3A8A, #0284C7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        text-align: center;
        padding-top: 15px;
        padding-bottom: 5px;
        letter-spacing: -0.5px;
    }
    .sub-text {
        font-size: 16px;
        color: #475569;
        text-align: center;
        font-weight: 600;
        margin-bottom: 30px;
    }
    .free-badge {
        background: linear-gradient(135deg, #059669, #10B981);
        color: white;
        padding: 5px 12px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 13px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .card-container {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.markdown('<p class="main-header">🌐 Global Professional Services Hub</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">AI-Powered Enterprise Transcription, Translation, Proofreading & ATS CV Optimization</p>', unsafe_allow_html=True)

st.markdown("---")

# --- SIDEBAR: CONFIGURATION & AUTHENTICATION ---
st.sidebar.header("⚙️ Platform Control Center")

# API Key configuration for Real AI
api_key_input = st.sidebar.text_input("Enter Gemini API Key (or use system default):", type="password")
if api_key_input:
    os.environ["GEMINI_API_KEY"] = api_key_input

st.sidebar.markdown("---")
st.sidebar.header("🔐 Admin Security")
admin_passcode = st.sidebar.text_input("Admin Passcode (Free Testing):", type="password")
is_admin = (admin_passcode == "admin123")

if is_admin:
    st.sidebar.success("🔓 Admin Mode Active (100% Free)")

st.sidebar.markdown("---")
st.sidebar.header("📂 Select Service")
service_choice = st.sidebar.selectbox(
    "Choose what you need:",
    [
        "🌍 AI Document Translation",
        "🎙️ Audio / Video Transcription",
        "📄 ATS CV Generation & Optimization",
        "✉️ Cover Letter Generation",
        "✍️ Text Proofreading & Polishing",
        "⚙️ Admin Dashboard"
    ]
)

# Language Lists with English First
ENGLISH_PRIMARY = ["🇺🇸/🇬🇧 English (US/UK)"]
ETHIOPIAN_LANGUAGES = [
    "🇪🇹 Amharic (አማርኛ)",
    "🇪🇹 Afaan Oromoo (Oromiffa)",
    "🇪🇹 Tigrinya (ትግርኛ)",
    "🇪🇹 Somali (Soomaali)",
    "🇪🇹 Sidama",
    "🇪🇹 Wolaytta",
    "🇪🇹 Gurage"
]
GLOBAL_LANGUAGES = [
    "🇸🇦 Arabic (العربية)",
    "🇫🇷 French (Français)",
    "🇨🇳 Mandarin Chinese (中文)",
    "🇪🇸 Spanish (Español)",
    "🇩🇪 German (Deutsch)",
    "🇮🇹 Italian (Italiano)"
]
ALL_LANGUAGES = ["✨ Auto-Detect Language"] + ENGLISH_PRIMARY + ETHIOPIAN_LANGUAGES + GLOBAL_LANGUAGES
TARGET_LANG_LIST = ENGLISH_PRIMARY + ETHIOPIAN_LANGUAGES + GLOBAL_LANGUAGES

# --- ADMIN DASHBOARD VIEW ---
if service_choice == "⚙️ Admin Dashboard":
    st.subheader("⚙️ Enterprise Management Dashboard")
    if is_admin:
        st.markdown('<span class="free-badge">ADMIN PRIVILEGES GRANTED</span>', unsafe_allow_html=True)
        st.markdown("""
        * **System Status:** Fully Online & AI-Connected
        * **Active Telebirr Account:** `0916884912` (Belayhun Adefrese Metaferia)
        * **Active CBE Account:** `1000296269488` (Leamare Branch, Lem Hotel Area, Addis Ababa)
        * **International Payer Channels:** Remitly, Wave, WorldRemit, Payone
