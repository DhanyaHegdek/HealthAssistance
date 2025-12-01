
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path='../../.env')

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY","")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY","")
PINECONE_ENV = os.getenv("PINECONE_ENV","")
PINECONE_INDEX = os.getenv("PINECONE_INDEX","mh-assistant")
DATABASE_URL = os.getenv("DATABASE_URL","sqlite:///./backend/dev.db")
CRISIS_KEYWORDS = ["kill myself","suicide","want to die","end it"]
HF_EMOTION_MODEL = "j-hartmann/emotion-english-distilroberta-base"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

