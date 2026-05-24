import os
import argparse
from scanner import CodeScanner
from memory import RepositoryMemory
from generator import DocGenerator
from git_manager import GitManager

def process_repository(repo_path):
    print("="*60)
    print(f"🚀 DocuMind AI: Starting analysis for {repo_path}")
    print("="*60)
    
    # 1. Initialize Modules
    scanner = CodeScanner(repo_path)
    memory = RepositoryMemory()
    generator = DocGenerator()
    git_manager = GitManager(repo_path)
    
    # 2. Scan Repository
    files = scanner.analyze_structure()
    print(f"📄 Found {len(files)} files to analyze.")
    
    # 3. Extract AST & Embed in Memory
    ast_data_collection = []
    file_contents = ""
    
    for file in files:
        if file.endswith('.py'):
            ast_data = scanner.extract_ast(file)
            if ast_data:
                ast_data_collection.append(ast_data)
        
        # Read content for memory and README generation context
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                memory.embed_file(file, content)
                # Keep a snippet for the README generator
                file_contents += f"\n--- {os.path.basename(file)} ---\n"
                file_contents += content[:500] + "...\n" # Only pass first 500 chars to save tokens
        except Exception as e:
            print(f"⚠️ Could not read {file}: {e}")
            
    # 4. Generate Documentation via LLM
    print("\n🧠 Invoking LLM to generate documentation...")
    readme_content = generator.generate_readme(
        repo_structure=[os.path.basename(f) for f in files],
        file_contents=file_contents
    )
    
    modules_content = generator.generate_api_specs(ast_data_collection)
    
    # 5. Write to File
    readme_path = os.path.join(repo_path, "README.md")
    modules_path = os.path.join(repo_path, "MODULES.md")
    
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    with open(modules_path, "w", encoding="utf-8") as f:
        f.write(modules_content)
        
    print(f"✅ Generated {readme_path}")
    print(f"✅ Generated {modules_path}")
    
    # 6. Commit Changes
    git_manager.commit_docs()
    
    print("\n🎉 DocuMind AI process complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DocuMind AI Agent")
    parser.add_argument("--repo", type=str, default=".", help="Path to the repository to analyze")
    args = parser.parse_args()
    
    # Convert to absolute path
    abs_path = os.path.abspath(args.repo)
    if not os.path.exists(abs_path):
        print(f"❌ Path does not exist: {abs_path}")
    else:
        process_repository(abs_path)
