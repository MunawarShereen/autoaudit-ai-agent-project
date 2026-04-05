import os

folders = [
    "app/api/routes",
    "app/core",
    "app/models",
    "app/services/ai_agents",
    "app/utils",
    "data/cloned_repos"
]

files = [
    "app/__init__.py",
    "app/main.py",
    "app/api/__init__.py",
    "app/api/routes/__init__.py",
    "app/api/routes/audit.py",
    "app/api/routes/github.py",
    "app/core/__init__.py",
    "app/core/config.py",
    "app/models/__init__.py",
    "app/models/request_schemas.py",
    "app/models/response_schemas.py",
    "app/services/__init__.py",
    "app/services/github_service.py",
    "app/services/vector_db.py",
    "app/services/ai_agents/__init__.py",
    "app/services/ai_agents/gemini_client.py",
    "app/services/ai_agents/auditor_agent.py",
    "app/services/ai_agents/refactor_agent.py",
    "app/services/ai_agents/orchestrator.py",
    "app/utils/__init__.py",
    "app/utils/file_parser.py",
    "app/utils/chunking.py",
    ".env",
    ".gitignore",
    "requirements.txt",
    "README.md"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

for file in files:
    with open(file, 'w') as f:
        pass

print("Project structure created successfully!")