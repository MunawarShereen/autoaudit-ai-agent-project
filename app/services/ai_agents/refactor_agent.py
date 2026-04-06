from app.services.ai_agents.gemini_client import get_gemini_model
from langchain_core.prompts import ChatPromptTemplate

def refactor_code(file_name: str, original_code: str, audit_report: str):
    llm = get_gemini_model()
    
    system_template = """
    You are an expert Full-Stack Developer. Your goal is to fix issues in the provided code based on an Audit Report.
    
    Rules:
    1. Maintain the original logic unless it's broken.
    2. Follow best practices (PEP8, clean code).
    3. ONLY return the code. Do not include explanations, markdown blocks, or extra text.
    """
    
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_template),
        ("user", "File: {file_name}\n\nOriginal Code:\n{code}\n\nAudit Report:\n{report}")
    ])
    
    chain = prompt_template | llm
    response = chain.invoke({
        "file_name": file_name, 
        "code": original_code, 
        "report": audit_report
    })
    
    return response.content