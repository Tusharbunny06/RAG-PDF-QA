# ===============================
# app.py (Backend)
# ===============================
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import faiss
import numpy as np

# ===============================
# Load Models
# ===============================
def load_models():
    embed_model = SentenceTransformer("multi-qa-mpnet-base-dot-v1")
    gen_qa = pipeline("text2text-generation", model="google/flan-t5-large")
    return embed_model, gen_qa

embed_model, gen_qa = load_models()

# ===============================
# Globals
# ===============================
chunks = []
metadata = []
index = None

# ===============================
# Chunking
# ===============================
def chunk_text(text, chunk_size=3000, overlap=500):
    text = text.replace("\n", " ")
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if len(chunk) > 100:
            chunks.append(chunk)
        start = end - overlap
    return chunks

# ===============================
# Load PDF
# ===============================
def load_pdf(pdf_path):
    global chunks, metadata, index
    chunks = []
    metadata = []

    reader = PdfReader(pdf_path)
    for page_no, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if not text or len(text.strip()) < 50:
            continue
        page_chunks = chunk_text(text)
        for ch in page_chunks:
            chunks.append(ch)
            metadata.append({"page": page_no, "id": len(chunks) - 1})

    embeddings = embed_model.encode(
        chunks, convert_to_numpy=True, normalize_embeddings=True, show_progress_bar=True
    ).astype(np.float32)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return len(chunks)

# ===============================
# Search
# ===============================
def search(query, top_k=5):
    query_vec = embed_model.encode([query], convert_to_numpy=True, normalize_embeddings=True).astype(np.float32)
    _, idxs = index.search(query_vec, top_k)
    results = []
    for i in idxs[0]:
        results.append({
            "text": chunks[i],
            "page": metadata[i]["page"],
            "id": metadata[i]["id"]
        })
    return results

# ===============================
# Generative QA
# ===============================
def answer_question(question, top_k=5):
    retrieved = search(question, top_k=top_k)
    context = " ".join([r['text'] for r in retrieved])
    prompt = f"Answer the question based on the context below.\nContext: {context}\nQuestion: {question}\nAnswer:"
    output = gen_qa(prompt, max_length=300)
    answer = output[0]['generated_text']
    source_page = retrieved[0]['page'] if retrieved else None
    return answer, source_page
