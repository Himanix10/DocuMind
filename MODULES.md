# 📦 Codebase Modules & Architecture: DocuMind AI

This document details the modules that form the core of **DocuMind AI** and how they interact to achieve autonomous technical documentation generation.

---

## 🗺️ Module Overview

```
DocuMind/
│
├── agent.py               # Core Orchestrator
├── scanner.py             # AST Parser & Directory Walk
├── memory.py              # ChromaDB Semantic Code Embeddings
├── generator.py           # Groq LLaMA-3.3 LLM Prompting
├── git_manager.py         # Git Branching, Commits, & PR push
└── webhook_server.py      # FastAPI REST Endpoints & Webhook receiver
```

---

## 🧩 Detailed Module Specifications

### 1. Core Orchestrator: `agent.py`
The orchestrator is the entrypoint. It initiates each component sequentially, ensuring data flows correctly between scanner, memory, generator, and Git.
*   **Key Function**: `process_repository(repo_path, repo_full_name)`
*   **Workflow**:
    1.  Scans local target repository path.
    2.  Extracts AST for Python files and embeds files into ChromaDB memory.
    3.  Passes structural and code context to the LLM generator.
    4.  Writes generated Markdown to target files.
    5.  Triggers GitManager to commit and open a PR.

### 2. AST & Directory Scanner: `scanner.py`
Recursively walks through project directories, parsing files to extract file structures and performing static syntax analysis.
*   **Class**: `CodeScanner`
*   **Key Methods**:
    *   `analyze_structure()`: Scans the directory and filters out ignored folders (like `.venv`, `node_modules`, `.git`).
    *   `extract_ast(file_path)`: Uses Python's native `ast` module to statically inspect python files, parsing top-level classes, methods, functions, and their docstrings.

### 3. Vector Memory System: `memory.py`
Enables the system to search codebase context semantically rather than just by simple keyword matching.
*   **Class**: `RepositoryMemory`
*   **Key Methods**:
    *   `embed_file(file_path, content)`: Chunks source code files and upserts them into a persistent vector database (ChromaDB).
    *   `semantic_search(query, n_results)`: Returns relevant code snippets matching any design or architecture query.

### 4. Technical Writer & LLM Engine: `generator.py`
Leverages Groq's high-speed API to prompt the highly capable `llama-3.3-70b-versatile` model.
*   **Class**: `DocGenerator`
*   **Key Methods**:
    *   `generate_readme(repo_structure, file_contents)`: Prompts the model with the directory architecture and key code files to construct a premium, complete `README.md`.
    *   `generate_api_specs(ast_data)`: Synthesizes class trees and method footprints into a detailed `MODULES.md`.

### 5. Git Automation Manager: `git_manager.py`
Wraps the `GitPython` library and `PyGithub` to perform isolated version control safely.
*   **Class**: `GitManager`
*   **Key Methods**:
    *   `create_branch(branch_name)`: Checks out `main`, pulls changes, and cuts a new unique branch.
    *   `commit_docs(message)`: Stages modified documentations (`README.md`, `MODULES.md`, `API_SPECS.md`) and commits them if changes are present.
    *   `push_and_create_pr(branch_name, title, body, repo_full_name)`: Pushes the branch using a safe authenticated remote and opens a pull request.

### 6. Event Gateway Server: `webhook_server.py`
FastAPI REST API that allows remote services (like the React dashboard or GitHub webhooks) to call the agent.
*   **Key Endpoints**:
    *   `GET /`: Returns health check and online status.
    *   `POST /trigger`: Receives manual trigger payloads containing the repository name, dynamically cloning the repo if it's running in cloud-mode, and running the agent in a background thread.
    *   `POST /webhook`: Listens for GitHub repository push events to trigger autonomous runs automatically.