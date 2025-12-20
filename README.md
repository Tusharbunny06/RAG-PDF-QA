📄 PDF Question Answering System (RAG)

An end-to-end Retrieval-Augmented Generation (RAG) system that allows users to upload PDF documents and ask questions. Relevant content is retrieved using vector search (FAISS), and answers are generated using a transformer-based language model via a Streamlit UI.

🚀 Features

Upload and process PDF documents

Automatic text chunking with overlap

Dense embeddings using Sentence Transformers

Fast semantic search with FAISS

LLM-based answer generation

Interactive Streamlit frontend

Displays approximate source page for answers

🧠 Tech Stack

Python

Streamlit (Frontend)

PyPDF (PDF parsing)

Sentence-Transformers (Embeddings)

FAISS (Vector database)

Transformers (Flan-T5) (Answer generation)

NumPy

📁 Project Structure
rag_project/
│── 1_backend/
│   └── app.py
│── 2_frontend/
│   └── ui.py
│── requirements.txt
│── .gitignore
│── README.md📌 
Future Improvements

Support for multiple PDFs

Persistent vector storage

Cloud deployment

API-based backend

Source highlighting

👤 Author

P.S. Tushar
Data Science Student
