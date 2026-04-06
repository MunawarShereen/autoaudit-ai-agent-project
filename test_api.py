import requests
import time

# Aapki FastAPI application ka URL
API_URL = "http://127.0.0.1:8000/api/start-audit-and-fix"

# YAHAN APNI GITHUB TEST REPO KA LINK DALEIN 👇
TARGET_REPO_URL = "https://github.com/MunawarShereen/ai-auditor-test"

def run_test():
    print(f"🚀 Starting AI Audit for: {TARGET_REPO_URL}")
    print("⏳ Please wait, AI is cloning, analyzing, refactoring, and opening a PR...")
    
    start_time = time.time()
    
    # API ko request bhejna
    payload = {"repo_url": TARGET_REPO_URL}
    
    try:
        response = requests.post(API_URL, json=payload, timeout=60) # 60 seconds timeout kyunki AI time leta hai
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ AI Process Completed Successfully!\n")
            print("-" * 50)
            
            for result in data.get("results", []):
                print(f"📄 File Analyzed: {result['file']}")
                print(f"🐛 Issues Found:\n{result['original_issue']}\n")
                print(f"✨ PR Link: {result['pr_url']}")
                print("-" * 50)
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        
    end_time = time.time()
    print(f"⏱️ Total Time Taken: {round(end_time - start_time, 2)} seconds")

if __name__ == "__main__":
    run_test()