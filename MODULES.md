# MODULES
## Overview
The DocuMind project consists of several modules, each responsible for a specific functionality. This document provides an overview of the purpose and functionality of each module.

## Agent Module
### agent.py
The agent module contains a single function, `process_repository`, which is currently undocumented. Further information about its purpose and usage is not available.

## Generator Module
### generator.py
The generator module contains a class, `DocGenerator`, which is responsible for generating documentation. The class has the following methods:
* `__init__`: Initializes the `DocGenerator` object.
* `generate_readme`: Generates a comprehensive README.md based on the repository contents.
* `generate_api_specs`: Generates an MODULES.md or API_SPECS.md based on the extracted AST data.

## Git Manager Module
### git_manager.py
The git manager module contains a class, `GitManager`, which handles Git-related operations. The class has the following methods:
* `__init__`: Initializes the `GitManager` object.
* `create_branch`: Creates and checks out a new branch for documentation updates.
* `commit_docs`: Stages and commits changes to the current branch.
* `push_and_create_pr`: Pushes the local branch and opens a Pull Request using PyGithub.

## Memory Module
### memory.py
The memory module contains a class, `RepositoryMemory`, which is responsible for embedding files and searching for semantic matches. The class has the following methods:
* `__init__`: Initializes the `RepositoryMemory` object.
* `embed_file`: Embeds a file's content into the vector DB for semantic search.
* `semantic_search`: Searches the codebase for semantic matches to provide context to the LLM.

## Scanner Module
### scanner.py
The scanner module contains a class, `CodeScanner`, which analyzes the repository structure and extracts AST data. The class has the following methods:
* `__init__`: Initializes the `CodeScanner` object.
* `analyze_structure`: Returns a list of all relevant files in the repository.
* `extract_ast`: Extracts classes, functions, and docstrings from a Python file.

## Webhook Server Module
### webhook_server.py
The webhook server module is currently empty and does not contain any classes or functions.