import os
from langchain_groq import ChatGroq
from app.core.config import settings

def get_gemini_model():
    groq_api_key = os.getenv("GROQ_API_KEY")
    
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY is missing in .env file!")
        
    # Naya aur latest supported model add kar diya gaya hai
    llm = ChatGroq(
        api_key=groq_api_key,
        model_name="llama-3.3-70b-versatile", # <-- Sirf ye line change hui hai
        temperature=0.2
    )
    return llm