from fastapi import APIRouter, HTTPException
from app.models.request_schemas import AuditRequest
from app.services.github_service import clone_repository, create_pull_request
from app.utils.file_parser import read_codebase
from app.services.ai_agents.auditor_agent import analyze_code_file
from app.services.ai_agents.refactor_agent import refactor_code # Make sure this file exists!
import time
router = APIRouter()

@router.post("/start-audit")
def start_audit(request: AuditRequest):
    """Purana endpoint sirf audit karne ke liye"""
    try:
        repo_path = clone_repository(str(request.repo_url))
        code_data = read_codebase(repo_path)
        
        audit_results = []
        for file in code_data[:3]:
            report = analyze_code_file(file['file_path'], file['content'])
            audit_results.append({
                "file": file['file_path'],
                "audit_report": report
            })

        return {
            "status": "success",
            "repo_url": str(request.repo_url),
            "findings": audit_results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/start-audit-and-fix")
def start_audit_and_fix(request: AuditRequest):
    repo_path = clone_repository(str(request.repo_url))
    code_data = read_codebase(repo_path)
    
    final_results = []

    for file in code_data[:1]: 
        print(f"🔍 Auditing file: {file['file_path']}...")
        
        # 1. Audit
        report = analyze_code_file(file['file_path'], file['content'])
        
        print("Waiting 5 seconds to respect API rate limits...")
        time.sleep(5) 
        
        # 2. Refactor
        print(f"🛠️ Refactoring file: {file['file_path']}...")
        fixed_code = refactor_code(file['file_path'], file['content'], report)
        
        # 3. Action
        print(f"🚀 Creating GitHub PR for: {file['file_path']}...")
        
        pr_url = create_pull_request(str(request.repo_url), file['file_path'], fixed_code)

        final_results.append({
            "file": file['file_path'],
            "original_issue": report,
            "fixed_code_snippet": fixed_code[:200] + "...", 
            "pr_url": pr_url
        })

    return {"status": "success", "results": final_results}

    """Naya endpoint jo Audit + Refactor + PR Create karega"""
    try:
        # 1. Clone Repo
        repo_path = clone_repository(str(request.repo_url))
        
        # 2. Read Code
        code_data = read_codebase(repo_path)
        
        if not code_data:
            return {"status": "error", "message": "No code files found in this repository."}
            
        final_results = []

        # 3. Process Only 1 File for testing (taake time kam lagay)
        for file in code_data[:1]: 
            print(f"🔍 Auditing file: {file['file_path']}...")
            report = analyze_code_file(file['file_path'], file['content'])
            
            time.sleep(5)
            
            print(f"🛠️ Refactoring file: {file['file_path']}...")
            fixed_code = refactor_code(file['file_path'], file['content'], report)
            
            print(f"🚀 Creating GitHub PR for: {file['file_path']}...")
            pr_url = create_pull_request(
                repo_url=str(request.repo_url), 
                file_path=file['file_path'], 
                new_content=fixed_code, 
                branch_name="ai-refactor-fix" # Branch ka naam
            )

            final_results.append({
                "file": file['file_path'],
                "original_issue": report,
                "fixed_code_snippet": fixed_code[:150] + "\n... (code truncated) ...", 
                "pr_url": pr_url
            })

        return {"status": "success", "results": final_results}
        
    except Exception as e:
        print(f"Error occurred: {str(e)}") # Terminal mein error print karega
        raise HTTPException(status_code=500, detail=str(e))