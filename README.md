# DocuMind AI
## Autonomous Technical Documentation Agent

DocuMind AI is an intelligent agent designed to reduce developer documentation effort by 90%. It continuously analyzes software repositories, APIs, pull requests, deployment logs, and architecture changes to automatically generate, update, optimize, and synchronize developer documentation with production-level accuracy.

## Project Overview
DocuMind AI is an agentic system that monitors codebases, understands deep architectural context through semantic search and AST parsing, and automatically generates or updates documentation to match the current state of the codebase. The system is designed to reduce the burden of documentation on developers, allowing them to focus on writing code.

## Architecture
The architecture of DocuMind AI is based on a modular design, with each module responsible for a specific function:
* `agent.py`: The central orchestration layer, responsible for coordinating the flow of data between modules.
* `scanner.py`: Scans the repository to understand the folder structure and identify relevant files.
* `memory.py`: Embeds file contents into a vector database for semantic search.
* `generator.py`: Generates documentation based on the repository structure and file contents.
* `git_manager.py`: Manages Git operations, including committing changes and pushing updates to the repository.
* `webhook_server.py`: Listens for incoming webhook events and triggers the analysis loop.

## Tech Stack
The tech stack used in DocuMind AI includes:
* Python 3.x
* Groq for natural language processing
* ChromaDB for vector database management
* GitPython for Git operations
* FastAPI for building the webhook server
* React and Vite for the frontend

## Setup Instructions
To set up DocuMind AI, follow these steps:
1. Clone the repository using `git clone`.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Set up the environment variables:
	* `GROQ_API_KEY`: Your Groq API key.
	* `GITHUB_TOKEN`: Your GitHub token.
4. Start the webhook server using `uvicorn webhook_server:app --host 0.0.0.0 --port 8000`.
5. Configure the webhook in your GitHub repository settings to point to `http://localhost:8000/api/v1/webhooks/github`.

## Features
* **Contextual Understanding:** Scans repositories recursively to understand folder structures, module dependencies, and code semantics.
* **Automated Documentation:** Generates high-quality documentation based on the repository structure and file contents.
* **Semantic Search:** Embeds file contents into a vector database for semantic search and retrieval.
* **Git Integration:** Commits changes and pushes updates to the repository using GitPython.

## Getting Started
To get started with DocuMind AI, simply clone the repository and follow the setup instructions. You can then configure the webhook in your GitHub repository settings to point to the webhook server. Once configured, DocuMind AI will automatically generate and update documentation for your repository.