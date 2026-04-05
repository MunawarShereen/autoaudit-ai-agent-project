from fastapi import FastAPI
from app.services.ai_agents.gemini_client import get_gemini_model
from app.api.routes import audit # <-- Ye line add ki hai

app = FastAPI(
    title="AI Code Auditor API",
    description="Autonomous Agent for Code Review and Refactoring"
)

# 👇 Router ko yahan include kar diya
app.include_router(audit.router, prefix="/api", tags=["Audit"])

@app.get("/")
def read_root():
    return {"message": "AI Code Auditor Backend is Running! 🚀"}

@app.get("/test-ai")
def test_ai_connection():
    # ... (purana code waisa hi rahega)
    try:
        llm = get_gemini_model()
        response = llm.invoke("Say 'Hello, System is Ready!' if you are active.")
        return {"status": "success", "ai_response": response.content}
    except Exception as e:
        return {"status": "error", "message": str(e)}