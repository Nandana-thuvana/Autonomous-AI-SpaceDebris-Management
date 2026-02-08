from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_PATH = os.path.join(BASE_DIR, "knowledge.txt")
DB_PATH = os.path.join(BASE_DIR, "vector_db")

with open(KNOWLEDGE_PATH, "r", encoding="utf-8") as f:
    text = f.read()

splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
texts = splitter.split_text(text)

# ⚠️ VERY IMPORTANT — remember this line exactly
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.from_texts(texts, embeddings)

db.save_local(DB_PATH)

print("✅ Vector DB created at:", DB_PATH)
