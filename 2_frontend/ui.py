# ===============================
# ui.py (Frontend)
# ===============================
import streamlit as st
import sys
import os

# Add 1_backend folder to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../1_backend")))

from app import load_pdf, answer_question  # Import backend functions

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
st.markdown("<h1 style='text-align:center;color:#4B0082;'>📄 PDF QA System</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ===============================
# Sidebar Instructions
# ===============================
with st.sidebar:
    st.header("ℹ️ Instructions")
    st.write("""
    1. Upload a PDF document.  
    2. Type your question in the input box.  
    3. The app will return a generative answer.  
    4. Source page is approximate.  
    """)

# ===============================
# PDF Upload
# ===============================
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    with st.spinner("Processing PDF..."):
        # Save uploaded PDF temporarily
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())
        # Load PDF using backend function
        num_chunks = load_pdf("temp.pdf")
        st.success(f"✅ PDF processed with {num_chunks} chunks.")

st.markdown("---")
question = st.text_input("💬 Ask a question:")

# ===============================
# Display Answer
# ===============================
if uploaded_file and question:
    with st.spinner("Generating answer..."):
        answer, page = answer_question(question, top_k=5)

    col1, col2 = st.columns([3, 1])

    # Transparent box for answer
    col1.markdown(
        f"<div style='padding:10px; border:1px solid #4B0082; border-radius:5px;'>"
        f"<b>Answer:</b> {answer}</div>",
        unsafe_allow_html=True
    )

    # Transparent box for source page
    if page:
        col2.markdown(
            f"<div style='padding:10px; border:1px solid #4B0082; border-radius:5px;'>"
            f"<b>Approx. Source Page:</b> {page}</div>",
            unsafe_allow_html=True
        )

st.markdown("<hr>", unsafe_allow_html=True)
