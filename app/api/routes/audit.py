from fastapi import APIRouter, HTTPException
from app.models.request_schemas import AuditRequest
from app.services.github_service import clone_repository
from app.utils.file_parser import read_codebase
from app.services.ai_agents.auditor_agent import analyze_code_file # <-- New Import

router = APIRouter()

@router.post("/start-audit")
def start_audit(request: AuditRequest):
    try:
        # Step 1: Repo Clone
        repo_path = clone_repository(str(request.repo_url))

        # Step 2: Code files read
        code_data = read_codebase(repo_path)
        
        audit_results = []

        # Step 3: Har file ko AI se audit karwana (Top 3 files for testing)
        for file in code_data[:3]: # Abhi ke liye sirf pehli 3 files check kar rahe hain
            print(f"Auditing: {file['file_path']}")
            report = analyze_code_file(file['file_path'], file['content'])
            audit_results.append({
                "file": file['file_path'],
                "audit_report": report
            })

        return {
            "status": "success",
            "repo_url": str(request.repo_url),
            "total_files_analyzed": len(audit_results),
            "findings": audit_results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))