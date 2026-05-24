# 🧠 DocuMind AI

### *Autonomous Technical Documentation Agent*

DocuMind AI is an autonomous, agentic system that continuously monitors repositories, parses complex codebases using semantic search and AST analysis, and auto-generates premium-grade technical documentation (`README.md`, `MODULES.md`, `API_SPECS.md`). It keeps your documentation perfectly synchronized with your actual code by autonomously opening Pull Requests when code changes are detected.

---

## 🌟 Key Features

*   🔄 **Continuous Autonomous Scanning**: Watches your repositories and triggers automatically on GitHub push events via webhooks, or manually with one-click from a gorgeous glassmorphic web UI.
*   🧠 **Deep Contextual Retrieval**: Embeds the codebase into a vector database (ChromaDB) to retrieve semantic context, ensuring the AI understands file relationships and architectural flows.
*   🌳 **AST Parsing**: Extracts abstract syntax trees (ASTs) of functions, methods, and classes to build detailed API specifications dynamically.
*   🐙 **Seamless Pull Requests**: Intelligently creates isolated branches (`documind/auto-update-...`), stages and commits only documentation updates, and opens clean, ready-to-merge PRs on your GitHub repository.
*   ☁️ **Cloud Native & Zero Configuration**: Dynamically clones and handles repositories in memory or temporary dirs in the cloud. It runs fully standalone on platforms like Render, Railway, or locally.

---

## 🏗️ Architecture

```mermaid
flowchart TD
    subgraph Event Sources
        GH[GitHub / GitLab] -->|Webhook: Push/PR| API[API Gateway / FastAPI]
        UI[React Control Center] -->|Manual Trigger| API
    end
    
    subgraph DocuMind Core
        API -->|Trigger| CM[Context Manager]
        CM -->|Dynamic Clone / Pull| RS[Repository Scanner]
        RS -->|AST & Diff Analysis| Analyzer[Code Analyzer]
        Analyzer -->|Vector Embeddings| VDB[(Vector DB / ChromaDB)]
        VDB -.->|Semantic Context| CM
        CM -->|Contextual Prompt| LLM[LLM Engine / LLaMA-3.3-70B]
    end
    
    subgraph Delivery
        LLM -->|Generate Markdown| Gen[Doc Generator]
        Gen --> GM[Git Manager]
        GM -->|Open PR with Docs| GH
    end
end
```

---

## 🌐 Link to Access your Agent

You can host and run DocuMind AI in minutes. To submit this to **Product Space** for testing:

1.  **Direct UI Access**: Provide the URL to your deployed frontend (e.g., `https://documind-ai.vercel.app` or your local server address).
2.  **Interactive Trigger**: Open the Control Center, input your target GitHub Repository, and click **Initialize Autonomous Scan**.
3.  **Autonomous Webhook URL**: Provide your hosted backend `/webhook` endpoint (e.g., `https://documind-api.onrender.com/webhook`) to be added as a GitHub Webhook for continuous automation on every push!

---

## 🚀 How to Run Locally

### 1. Prerequisite Keys
Make sure you have:
*   A **Groq API Key** (for lightning-fast LLaMA-3.3-70B generation)
*   A **GitHub Personal Access Token (PAT)** with `repo` access to clone and push PRs.

### 2. Backend Server Setup
From the root of the project:
```bash
# Clone the repository
git clone https://github.com/Himanix10/DocuMind.git
cd DocuMind

# Create environment file
copy .env.example .env
# Open .env and populate GITHUB_TOKEN and GROQ_API_KEY

# Install dependencies
pip install -r requirements.txt

# Start the autonomous agent server
python webhook_server.py
```
The server will start on `http://localhost:8000`.

### 3. Frontend Web Console Setup
From the `frontend` directory:
```bash
cd frontend

# Install node dependencies
npm install

# Run the UI development server
npm run dev
```
Open `http://localhost:5173` in your browser to view the premium dashboard.

---

## ☁️ 1-Click Cloud Deployment

### Backend (FastAPI Server)
You can deploy the backend to **Render**, **Railway**, or **Koyeb** directly from your GitHub fork:
1.  Connect your GitHub repository.
2.  Set the start command to: `uvicorn webhook_server:app --host 0.0.0.0 --port $PORT`
3.  Add environment variables:
    *   `GROQ_API_KEY`: Your Groq API token.
    *   `GITHUB_TOKEN`: Your GitHub Personal Access Token.

### Frontend (Vite App)
Deploy the frontend to **Vercel** or **Netlify**:
1.  Connect your GitHub repository, selecting the `frontend` folder as the root directory.
2.  Set the build command to: `npm run build`
3.  Set the output directory to: `dist`
4.  Add environment variable:
    *   `VITE_BACKEND_URL`: Your hosted backend URL (e.g., `https://documind-api.onrender.com`).