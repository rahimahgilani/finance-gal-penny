import os
from langchain_chroma import Chroma
from app.embeddings import get_embeddings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_DIR = os.path.join(BASE_DIR, "data", "chroma_db")

def create_vector_store(chunks, filename):
    # print(f"Using chroma dir: {CHROMA_DIR}")
    embeddings = get_embeddings()
    
    vector_store = Chroma(
        collection_name="pdf-embeddings",
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )
    
    vector_store.add_texts(chunks, metadatas=[{"source": filename} for _ in chunks])
    
    return vector_store

def load_vector_store():
    # print(f"Using chroma dir: {CHROMA_DIR}")
    embeddings = get_embeddings()
    vector_store = Chroma(
        collection_name="pdf-embeddings",
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )
    return vector_store

