import os
import argparse
import uuid
from scanner import CodeScanner
from memory import RepositoryMemory
from generator import DocGenerator
from git_manager import GitManager

def process_repository(repo_path, repo_full_name="Himanix10/india-restaurant-finder"):
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
    
    # 3. Branch for documentation (Autonomous flow)
    branch_name = f"documind/auto-update-{uuid.uuid4().hex[:6]}"
    git_manager.create_branch(branch_name)
    
    # 4. Extract AST & Embed in Memory
    ast_data_collection = []
    file_contents = ""
    
    for file in files:
        if file.endswith('.py'):
            ast_data = scanner.extract_ast(file)
            if ast_data:
                ast_data_collection.append(ast_data)
        
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                memory.embed_file(file, content)
                file_contents += f"\n--- {os.path.basename(file)} ---\n"
                file_contents += content[:500] + "...\n" 
        except Exception as e:
            print(f"⚠️ Could not read {file}: {e}")
            
    # 5. Generate Documentation via LLM
    print("\n🧠 Invoking LLM to generate documentation...")
    readme_content = generator.generate_readme(
        repo_structure=[os.path.basename(f) for f in files],
        file_contents=file_contents
    )
    modules_content = generator.generate_api_specs(ast_data_collection)
    
    # 6. Write to File
    readme_path = os.path.join(repo_path, "README.md")
    modules_path = os.path.join(repo_path, "MODULES.md")
    
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    with open(modules_path, "w", encoding="utf-8") as f:
        f.write(modules_content)
        
    print(f"✅ Generated {readme_path}")
    print(f"✅ Generated {modules_path}")
    
    # 7. Commit & PR
    has_changes = git_manager.commit_docs()
    
    if has_changes:
        title = "docs: auto-update API and Architecture documentation"
        body = "### Generated autonomously by DocuMind AI 🧠\n\nI have detected code changes and updated the documentation accordingly."
        git_manager.push_and_create_pr(branch_name, title, body, repo_full_name)
    else:
        print("ℹ️ No PR created since there were no changes.")
    
    print("\n🎉 DocuMind AI process complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DocuMind AI Agent")
    parser.add_argument("--repo", type=str, default=".", help="Path to the local repository to analyze")
    parser.add_argument("--github_repo", type=str, default="", help="e.g. Himanix10/india-restaurant-finder")
    args = parser.parse_args()
    
    abs_path = os.path.abspath(args.repo)
    if not os.path.exists(abs_path):
        print(f"❌ Path does not exist: {abs_path}")
    else:
        process_repository(abs_path, args.github_repo)
