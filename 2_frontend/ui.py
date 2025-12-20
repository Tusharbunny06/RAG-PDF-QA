# ===============================
# ui.py (Frontend)
# ===============================
import streamlit as st
import sys
import os
import tempfile

# -------------------------------
# Add 1_backend folder to Python path
# -------------------------------
BACKEND_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../1_backend")
)
sys.path.insert(0, BACKEND_PATH)

from app import load_pdf, answer_question  # backend functions

# ===============================
# Streamlit Page Config
# ===============================
st.set_page_config(
    page_title="PDF QA System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================
# UI Header
# ===============================
st.markdown(
    "<h1 style='text-align:center;color:#4B0082;'>📄 PDF QA System</h1>",
    unsafe_allow_html=True
)
st.markdown("<hr>", unsafe_allow_html=True)

# ===============================
# Sidebar Instructions
# ===============================
with st.sidebar:
    st.header("ℹ️ Instructions")
    st.write(
        """
        1. Upload a PDF document  
        2. Ask a question from the PDF  
        3. The system retrieves relevant context  
        4. Answer is generated using RAG  
        """
    )

# ===============================
# Session State
# ===============================
if "pdf_loaded" not in st.session_state:
    st.session_state.pdf_loaded = False

# ===============================
# PDF Upload
# ===============================
uploaded_file = st.file_uploader("📤 Upload PDF", type="pdf")

if uploaded_file and not st.session_state.pdf_loaded:
    with st.spinner("Processing PDF..."):
        # Save PDF safely (Streamlit Cloud compatible)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            temp_pdf_path = tmp.name

        num_chunks = load_pdf(temp_pdf_path)
        st.session_state.pdf_loaded = True

        st.success(f"✅ PDF processed successfully ({num_chunks} chunks)")

st.markdown("---")

# ===============================
# Question Input
# ===============================
question = st.text_input("💬 Ask a question from the PDF:")

# ===============================
# Display Answer
# ===============================
if st.session_state.pdf_loaded and question:
    with st.spinner("Generating answer..."):
        answer, page = answer_question(question, top_k=5)

    col1, col2 = st.columns([3, 1])

    col1.markdown(
        f"""
        <div style='padding:12px;border:1px solid #4B0082;border-radius:6px;'>
        <b>Answer:</b><br>{answer}
        </div>
        """,
        unsafe_allow_html=True
    )

    if page is not None:
        col2.markdown(
            f"""
            <div style='padding:12px;border:1px solid #4B0082;border-radius:6px;'>
            <b>Approx. Source Page:</b><br>{page}
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("<hr>", unsafe_allow_html=True)
