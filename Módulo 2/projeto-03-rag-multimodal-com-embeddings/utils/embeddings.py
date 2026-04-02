from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from dotenv import load_dotenv
import os 

load_dotenv()

GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

def cria_embeddings(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        api_key=GEMINI_API_KEY
    )

    vectorstore = InMemoryVectorStore.from_texts(
        chunks,
        embedding=embeddings
    )

    return vectorstore








