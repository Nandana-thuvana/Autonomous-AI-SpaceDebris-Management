import os
from google import genai

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "vector_db")

# Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Embeddings (same as used during DB creation)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.load_local(
    DB_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)


def ask_gemini(question: str) -> str:
    # Retrieve knowledge from FAISS
    docs = db.similarity_search(question, k=3)
    context = "\n".join([d.page_content for d in docs])

    prompt = f"""
You are an AI assistant for a Space Debris Clean-Up Planning System.

Use the project knowledge to explain ONLY about the object's orbital nature.

Do NOT explain anything about machine learning or the model.

Explain in three parts:
1) Orbital behavior of the object
2) Collision risk it creates
3) Proper clean-up strategy based on its orbit

PROJECT KNOWLEDGE:
{context}

QUESTION:
{question}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.candidates[0].content.parts[0].text
