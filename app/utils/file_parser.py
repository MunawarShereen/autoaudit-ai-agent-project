import os

# Kon si files padhni hain
ALLOWED_EXTENSIONS = {'.py', '.js', '.ts', '.java', '.cpp', '.c', '.html', '.css', '.md', '.ipynb'}
# Kon se folders ignore karne hain
IGNORE_DIRS = {'.git', 'node_modules', 'venv', 'env', '__pycache__', 'dist', 'build'}

def read_codebase(repo_path: str):
    code_files = []
    
    for root, dirs, files in os.walk(repo_path):
        # Ignore dirs ko hata do taake unke andar scan na kare
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in ALLOWED_EXTENSIONS:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # File ka relative path nikalte hain (e.g., 'src/main.py')
                        relative_path = os.path.relpath(file_path, repo_path)
                        code_files.append({
                            "file_path": relative_path, 
                            "content": content
                        })
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")
                    
    return code_files