# MODULES.md
## Overview
The DocuMind project consists of several modules, each responsible for a specific functionality. This document provides an overview of the purpose and functionality of each module.

## Agent Module
### agent.py
The agent module contains a single function, `process_repository`, which is currently undocumented. Further information about its purpose and usage is not available.

## Generator Module
### generator.py
The generator module contains a class, `DocGenerator`, which is responsible for generating documentation files.
#### DocGenerator Class
* `__init__`: Initializes the `DocGenerator` object.
* `generate_readme`: Generates a comprehensive README.md based on repository contents.
* `generate_api_specs`: Generates an MODULES.md or API_SPECS.md based on extracted AST data.

## Git Manager Module
### git_manager.py
The Git Manager module contains a class, `GitManager`, which handles Git-related operations.
#### GitManager Class
* `__init__`: Initializes the `GitManager` object.
* `create_branch`: Creates and checks out a new branch for documentation updates.
* `commit_docs`: Stages and commits changes to the current branch.
* `push_and_create_pr`: Pushes the local branch and opens a Pull Request using PyGithub.

## Memory Module
### memory.py
The Memory module contains a class, `RepositoryMemory`, which is responsible for embedding files and performing semantic searches.
#### RepositoryMemory Class
* `__init__`: Initializes the `RepositoryMemory` object.
* `embed_file`: Embeds a file's content into the vector DB for semantic search.
* `semantic_search`: Searches the codebase for semantic matches to provide context to the LLM.

## Scanner Module
### scanner.py
The Scanner module contains a class, `CodeScanner`, which analyzes the repository structure and extracts AST data.
#### CodeScanner Class
* `__init__`: Initializes the `CodeScanner` object.
* `analyze_structure`: Returns a list of all relevant files in the repository.
* `extract_ast`: Extracts classes, functions, and docstrings from a Python file.

## Webhook Server Module
### webhook_server.py
The Webhook Server module is currently empty and does not contain any functions or classes.