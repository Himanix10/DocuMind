import os
import ast

class CodeScanner:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.ignore_dirs = {'.git', '__pycache__', 'venv', '.venv', 'env', 'node_modules', '.documind_db'}
    
    def analyze_structure(self):
        """Returns a list of all relevant files in the repository."""
        print(f"🔍 Scanning directory structure at {self.repo_path}...")
        files_found = []
        for root, dirs, files in os.walk(self.repo_path):
            # Ignore specified directories
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]
            for file in files:
                if file.endswith('.py') or file.endswith('.md') or file.endswith('.json'):
                    files_found.append(os.path.join(root, file))
        return files_found
        
    def extract_ast(self, file_path):
        """Extracts classes, functions, and docstrings from a Python file."""
        if not file_path.endswith('.py'):
            return None
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            tree = ast.parse(content)
            
            entities = {
                "file": file_path,
                "docstring": ast.get_docstring(tree),
                "classes": [], 
                "functions": []
            }
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    entities["classes"].append({
                        "name": node.name,
                        "docstring": ast.get_docstring(node),
                        "methods": [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    })
                elif isinstance(node, ast.FunctionDef):
                    # Only grab top-level functions (not methods inside classes)
                    # A robust parser would track scope, but this is an MVP
                    entities["functions"].append({
                        "name": node.name,
                        "docstring": ast.get_docstring(node)
                    })
                    
            return entities
        except Exception as e:
            print(f"⚠️ Failed to parse AST for {file_path}: {e}")
            return None
