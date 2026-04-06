import os
import uuid
import time # <-- Time import add kiya
from git import Repo
from github import Github 
from app.core.config import settings 

CLONE_DIR = "data/cloned_repos"

def clone_repository(repo_url: str) -> str:
    repo_id = str(uuid.uuid4())[:8]
    target_path = os.path.join(CLONE_DIR, repo_id)
    if not os.path.exists(CLONE_DIR):
        os.makedirs(CLONE_DIR)
    print(f"Cloning {repo_url} into {target_path}...")
    Repo.clone_from(repo_url, target_path)
    return target_path

def extract_repo_name(repo_url: str) -> str:
    # URL ko saaf karta hai (trailing slashes aur .git ko remove karta hai)
    clean_url = repo_url.rstrip('/').replace('.git', '')
    parts = clean_url.split('/')
    return f"{parts[-2]}/{parts[-1]}"

def create_pull_request(repo_url: str, file_path: str, new_content: str, pr_title: str = "🚀 AI Code Refactor & Fixes"):
    if not settings.GITHUB_TOKEN:
        raise ValueError("GITHUB_TOKEN is missing in .env file!")

    try:
        print("Authenticating with GitHub...")
        g = Github(settings.GITHUB_TOKEN)
        
        repo_name = extract_repo_name(repo_url)
        repo = g.get_repo(repo_name)

        source_branch = repo.default_branch
        source_ref = repo.get_branch(source_branch)

        # FIX 1: Har dafa ek unique branch banayein taake collision na ho
        unique_id = str(uuid.uuid4())[:6]
        branch_name = f"ai-refactor-{unique_id}"
        
        print(f"Creating new branch: {branch_name}...")
        repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=source_ref.commit.sha)

        # FIX 2: Windows backslash (\) ko GitHub forward slash (/) mein convert karein
        github_file_path = file_path.replace("\\", "/")

        print(f"Fetching original file: {github_file_path}...")
        contents = repo.get_contents(github_file_path, ref=source_branch)

        print("Committing refactored code...")
        repo.update_file(
            path=contents.path,
            message=f"🤖 AI Refactor: Updated {github_file_path}",
            content=new_content,
            sha=contents.sha,
            branch=branch_name
        )

        print("Opening Pull Request...")
        pr_body = """
        ### 🤖 Autonomous AI Code Auditor
        This Pull Request was generated automatically by the AI Agent.
        
        **Changes Made:**
        - Fixed potential security/performance vulnerabilities identified in the audit.
        - Refactored code to meet standard best practices.
        """
        
        pr = repo.create_pull(
            title=pr_title,
            body=pr_body,
            head=branch_name,
            base=source_branch
        )
        
        print(f"✅ Success! PR opened at: {pr.html_url}")
        return pr.html_url

    except Exception as e:
        print(f"❌ Error creating Pull Request: {e}")
        return f"Error: {str(e)}"