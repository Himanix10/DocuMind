# Module Level Documentation: DocuMind AI

This document explains the core modules and internal logic of the **DocuMind AI** documentation agent.

## `agent.py`
**Purpose**: The central orchestration layer.
- `start_analysis_loop()`: Listens for incoming webhook events or scheduled cron jobs.
- `process_repository(repo_url)`: Coordinates the flow from scanning the repo, updating the vector memory, generating the docs, and committing the changes.
- **Agentic Behavior**: Contains the decision-making logic to determine *if* a documentation update is required based on the significance of the code changes.

## `scanner.py`
**Purpose**: Codebase ingestion and parsing.
- `analyze_structure(path)`: Recursively maps the directory structure, identifying key architectural layers (e.g., frontend, backend, database).
- `extract_ast(file)`: Parses Python/JS/TS files into Abstract Syntax Trees to extract function signatures, classes, and docstrings.
- `detect_diffs(old_commit, new_commit)`: Analyzes Git diffs to isolate modified logic, newly added modules, and deleted components.

## `generator.py`
**Purpose**: Interfaces with the LLM to write developer-friendly documentation.
- `generate_readme(context)`: Synthesizes high-level project goals, setup instructions, and tech stack into a `README.md`.
- `generate_api_specs(routes)`: Formats extracted API routes into standardized markdown, including endpoints, methods, parameters, request/response examples, and error cases.
- `update_stale_docs(existing_doc, changes)`: Intelligently merges new information into existing documentation without destroying custom developer notes.

## `memory.py`
**Purpose**: Manages long-term repository context.
- `embed_codebase()`: Chunks codebase files and converts them into embeddings.
- `semantic_search(query)`: Allows the agent (or users via a Q&A interface) to find relevant code snippets and architecture patterns.
- `track_architecture_evolution()`: Compares current architectural graphs with historical ones to automatically generate migration notes and changelogs.

## `git_manager.py`
**Purpose**: Handles repository version control operations.
- `clone_and_branch()`: Creates a secure workspace for documentation updates.
- `commit_changes(files_changed)`: Formats commit messages clearly (e.g., `docs: auto-update API specifications for v2.0`).
- `create_pull_request()`: Interfaces with the GitHub API to open a PR, complete with a summary of the documentation changes, affected modules, and any breaking changes detected.
