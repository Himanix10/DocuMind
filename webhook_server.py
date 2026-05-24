from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import threading
from agent import process_repository
import os
import shutil
import git

app = FastAPI()

# Add CORS middleware to allow React frontend to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for local hackathon demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_or_clone_repo(repo_path: str, repo_full_name: str) -> str:
    """
    Checks if the local repo path exists. If not, clones the repository
    dynamically into a temporary folder using the GITHUB_TOKEN.
    """
    # If the repo path is a valid local folder, use it
    if os.path.exists(repo_path) and os.path.isdir(os.path.join(repo_path, ".git")):
        print(f"📁 Using existing local repository path: {repo_path}")
        return os.path.abspath(repo_path)
    
    # Otherwise, clone it dynamically
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        print("⚠️ GITHUB_TOKEN not found in environment variables!")
        raise HTTPException(status_code=400, detail="GITHUB_TOKEN not configured on server.")
        
    temp_dir = os.path.abspath(os.path.join(os.getcwd(), "temp_repos", repo_full_name.replace("/", "_")))
    
    # Clean up old directory if it exists to get a fresh clone
    if os.path.exists(temp_dir):
        print(f"♻️ Temp directory exists at {temp_dir}. Cleaning it up for fresh clone...")
        try:
            shutil.rmtree(temp_dir)
        except Exception as e:
            print(f"⚠️ Failed to remove old temp directory: {e}")
            
    os.makedirs(os.path.dirname(temp_dir), exist_ok=True)
    
    clone_url = f"https://{github_token}@github.com/{repo_full_name}.git"
    print(f"📥 Cloning {repo_full_name} into {temp_dir}...")
    try:
        git.Repo.clone_from(clone_url, temp_dir)
        print("✅ Clone successful!")
        return temp_dir
    except Exception as e:
        print(f"❌ Failed to clone repository: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to clone repository: {str(e)}")

@app.get("/")
async def root():
    return {
        "status": "online", 
        "message": "🧠 DocuMind AI Webhook Server is running! Send GitHub POST requests to /webhook"
    }

@app.post("/trigger")
async def manual_trigger(request: Request):
    """
    Endpoint for the React Frontend to trigger a documentation scan manually.
    """
    payload = await request.json()
    repo_path = payload.get("repo_path", "../india-restaurant-finder")
    repo_full_name = payload.get("repo_full_name", "Himanix10/india-restaurant-finder")
    
    try:
        # Get local path or clone dynamically
        local_repo_path = get_or_clone_repo(repo_path, repo_full_name)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    print(f"\n🚀 [UI TRIGGER] Starting DocuMind background task for {local_repo_path}...")
    threading.Thread(target=process_repository, args=(local_repo_path, repo_full_name)).start()
    
    return {
        "status": "success", 
        "message": f"DocuMind started processing {repo_full_name}",
        "local_path": local_repo_path
    }

@app.post("/webhook")
async def github_webhook(request: Request):
    """
    Listens for GitHub push events.
    """
    payload = await request.json()
    
    # Check if this is a push event
    if "commits" in payload:
        print("\n🔔 [WEBHOOK] Received push event!")
        
        target_repo_full_name = payload.get("repository", {}).get("full_name", "Himanix10/india-restaurant-finder")
        default_local_path = os.getenv("TARGET_REPO_PATH", "../india-restaurant-finder")
        
        try:
            # Get local path or clone dynamically
            local_repo_path = get_or_clone_repo(default_local_path, target_repo_full_name)
        except Exception as e:
            print(f"❌ Webhook clone error: {e}")
            return {"status": "error", "message": f"Clone failed: {str(e)}"}
            
        print(f"🚀 [WEBHOOK] Triggering DocuMind background task for {local_repo_path}...")
        threading.Thread(target=process_repository, args=(local_repo_path, target_repo_full_name)).start()
        
        return {"status": "success", "message": f"DocuMind agent triggered for {target_repo_full_name}"}
        
    return {"status": "ignored", "message": "Not a push event"}

if __name__ == "__main__":
    print("🌐 Starting DocuMind Autonomous Webhook Server on port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)

