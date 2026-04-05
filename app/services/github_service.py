import os
import uuid
from git import Repo

CLONE_DIR = "data/cloned_repos"

def clone_repository(repo_url: str) -> str:
    # Har repo ke liye ek unique folder name banate hain
    repo_id = str(uuid.uuid4())[:8]
    target_path = os.path.join(CLONE_DIR, repo_id)

    # Agar clone directory nahi hai toh bana do
    if not os.path.exists(CLONE_DIR):
        os.makedirs(CLONE_DIR)

    print(f"Cloning {repo_url} into {target_path}...")
    
    # Git clone command
    Repo.clone_from(repo_url, target_path)
    
    return target_path