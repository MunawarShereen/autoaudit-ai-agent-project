from app.services.ai_agents.gemini_client import get_gemini_model
from langchain_core.prompts import ChatPromptTemplate

def analyze_code_file(file_name: str, code_content: str):
    llm = get_gemini_model()
    
    # System Prompt: AI ko batana ke wo kaun hai aur kya karna hai
    system_template = """
    You are an expert Senior Software Engineer and Security Researcher.
    Your task is to audit the following code file: {file_name}
    
    Look for:
    1. Security vulnerabilities (SQL Injection, XSS, Hardcoded Keys).
    2. Performance bottlenecks (Inefficient loops, memory leaks).
    3. Logical bugs or edge cases.
    4. Code quality improvements.

    Provide your response in a clear bullet-point format.
    """
    
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_template),
        ("user", "Here is the code content:\n\n{code}")
    ])
    
    # Chain create karna
    chain = prompt_template | llm
    
    # Gemini ko call karna
    response = chain.invoke({"file_name": file_name, "code": code_content})
    return response.content