import git
import os

class GitManager:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        print(f"🔧 Initializing Git Manager for {self.repo_path}...")
        try:
            self.repo = git.Repo(self.repo_path)
        except git.exc.InvalidGitRepositoryError:
            print(f"⚠️ {self.repo_path} is not a valid Git repository.")
            self.repo = None
            
    def commit_docs(self, message="docs: auto-generate documentation via DocuMind AI"):
        """Commits changes to the current repository."""
        if not self.repo:
            return False
            
        print(f"📦 Staging documentation changes in {self.repo_path}...")
        try:
            self.repo.git.add('.')
            
            # Check if there are changes
            if not self.repo.is_dirty(untracked_files=True):
                print("ℹ️ No documentation changes detected. Skipping commit.")
                return True
                
            print(f"💾 Committing: '{message}'")
            self.repo.index.commit(message)
            
            print("🚀 Git commit complete! (Note: Push is manual for MVP safety)")
            return True
        except Exception as e:
            print(f"⚠️ Git operation failed: {e}")
            return False
