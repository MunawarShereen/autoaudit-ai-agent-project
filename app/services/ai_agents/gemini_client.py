from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings

# Gemini 1.5 Pro model initialize kar rahe hain
def get_gemini_model():
    if not settings.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is missing in .env file!")
        
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        google_api_key=settings.GEMINI_API_KEY,
        temperature=0.2 # Temperature low rakhi hai taake code logic strict rahay
    )
    return llm