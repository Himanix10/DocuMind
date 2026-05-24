# DocuMind AI
## Autonomous Technical Documentation Agent

DocuMind AI is an intelligent agent designed to reduce developer documentation effort by 90%. It continuously analyzes software repositories, APIs, pull requests, deployment logs, and architecture changes to automatically generate, update, optimize, and synchronize developer documentation with production-level accuracy.

## Project Overview
DocuMind AI is a cutting-edge solution for automating technical documentation. It utilizes advanced technologies such as semantic search, AST parsing, and machine learning to understand the deep architectural context of a codebase and generate high-quality documentation.

## Architecture
The architecture of DocuMind AI is designed as an agentic system that monitors codebases and understands deep architectural context through semantic search and AST parsing. The system consists of several modules, each responsible for a specific functionality:

* **Agent Module**: The agent module contains a single function, `process_repository`, which is responsible for initializing the analysis of a repository.
* **Generator Module**: The generator module contains a class, `DocGenerator`, which is responsible for generating documentation based on the analysis of the repository.
* **Scanner Module**: The scanner module contains a class, `CodeScanner`, which is responsible for scanning the directory structure of a repository and analyzing its contents.
* **Git Manager Module**: The git manager module contains a class, `GitManager`, which is responsible for managing Git operations and interacting with the GitHub API.
* **Memory Module**: The memory module contains a class, `RepositoryMemory`, which is responsible for storing and retrieving information about a repository.

## Tech Stack
The tech stack used by DocuMind AI includes:

* **Python**: The primary programming language used for development.
* **Groq**: A machine learning platform used for generating documentation.
* **ChromaDB**: A vector database used for storing and retrieving information about a repository.
* **GitHub API**: Used for interacting with GitHub repositories and automating Git operations.
* **FastAPI**: A web framework used for building the webhook server.
* **React**: A JavaScript library used for building the frontend.

## Setup Instructions
To set up DocuMind AI, follow these steps:

1. **Install dependencies**: Run `npm install` to install the dependencies listed in `package.json`.
2. **Set environment variables**: Set the following environment variables:
	* `GROQ_API_KEY`: Your Groq API key.
	* `GITHUB_TOKEN`: Your GitHub token.
3. **Start the webhook server**: Run `uvicorn webhook_server:app --host 0.0.0.0 --port 8000` to start the webhook server.
4. **Configure the agent**: Configure the agent by modifying the `agent.py` file to point to your repository.
5. **Run the agent**: Run `python agent.py` to start the agent and begin analyzing your repository.

## API Integration
DocuMind AI interacts with several external APIs to orchestrate its autonomous documentation pipeline. The key integrations are:

* **GitHub API**: Used for monitoring repository events and automating Git operations.
* **Groq API**: Used for generating documentation.

## Webhook Integration
The webhook server listens for `push` and `pull_request` events from GitHub and triggers the analysis of the repository.

## Contributing
To contribute to DocuMind AI, please fork the repository and submit a pull request with your changes. Please ensure that your changes are well-documented and follow the existing code style.

## License
DocuMind AI is licensed under the MIT License. See `LICENSE` for details.