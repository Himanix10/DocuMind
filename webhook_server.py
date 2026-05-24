from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import threading
from agent import process_repository
import os

app = FastAPI()

# Add CORS middleware to allow React frontend to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for local hackathon demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    
    print(f"\n🚀 [UI TRIGGER] Starting DocuMind background task for {repo_path}...")
    threading.Thread(target=process_repository, args=(repo_path, repo_full_name)).start()
    
    return {"status": "success", "message": f"DocuMind started processing {repo_path}"}

@app.post("/webhook")
async def github_webhook(request: Request):
    """
    Listens for GitHub push events.
    """
    payload = await request.json()
    
    # Check if this is a push event
    if "commits" in payload:
        print("\n🔔 [WEBHOOK] Received push event!")
        
        target_repo = os.getenv("TARGET_REPO_PATH", "../india-restaurant-finder")
        target_repo_full_name = payload.get("repository", {}).get("full_name", "Himanix10/india-restaurant-finder")
        
        print(f"🚀 [WEBHOOK] Triggering DocuMind background task for {target_repo}...")
        threading.Thread(target=process_repository, args=(target_repo, target_repo_full_name)).start()
        
        return {"status": "success", "message": "DocuMind agent triggered"}
        
    return {"status": "ignored", "message": "Not a push event"}

if __name__ == "__main__":
    print("🌐 Starting DocuMind Autonomous Webhook Server on port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
