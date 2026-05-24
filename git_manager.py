import git
import os
import uuid
from github import Github
from dotenv import load_dotenv

load_dotenv()

class GitManager:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        print(f"🔧 Initializing Git Manager for {self.repo_path}...")
        try:
            self.repo = git.Repo(self.repo_path)
            self.github_token = os.getenv("GITHUB_TOKEN")
        except git.exc.InvalidGitRepositoryError:
            print(f"⚠️ {self.repo_path} is not a valid Git repository.")
            self.repo = None
            
    def create_branch(self, branch_name):
        """Creates and checks out a new branch for the documentation updates."""
        if not self.repo:
            return False
            
        print(f"🌿 Creating new branch: {branch_name}")
        try:
            # Make sure we're on main and pull latest before branching
            if "main" in self.repo.heads:
                self.repo.heads.main.checkout()
            
            new_branch = self.repo.create_head(branch_name)
            new_branch.checkout()
            return True
        except Exception as e:
            print(f"⚠️ Failed to create branch: {e}")
            return False

    def commit_docs(self, message="docs: auto-generate documentation via DocuMind AI"):
        """Stages and commits changes to the current branch."""
        if not self.repo:
            return False
            
        print(f"📦 Staging documentation changes in {self.repo_path}...")
        try:
            # Only add the generated documentation files to avoid massive staging if .venv is unignored
            self.repo.git.add('README.md')
            try:
                self.repo.git.add('MODULES.md')
            except Exception:
                pass
            try:
                self.repo.git.add('API_SPECS.md')
            except Exception:
                pass
            
            if not self.repo.is_dirty(untracked_files=True):
                print("ℹ️ No documentation changes detected. Skipping commit.")
                return False
                
            print(f"💾 Committing: '{message}'")
            self.repo.index.commit(message)
            return True
        except Exception as e:
            print(f"⚠️ Git commit failed: {e}")
            return False
            
    def push_and_create_pr(self, branch_name, title, body, repo_full_name):
        """Pushes the local branch and opens a Pull Request using PyGithub."""
        if not self.repo or not self.github_token:
            print("⚠️ Missing GITHUB_TOKEN or invalid repo. Cannot open PR.")
            return False
            
        print("🚀 Pushing branch to remote with authenticated token...")
        try:
            origin = self.repo.remote(name='origin')
            remote_url = list(origin.urls)[0]
            
            # Create a custom authenticated URL
            if remote_url.startswith("https://"):
                auth_url = remote_url.replace("https://", f"https://{self.github_token}@")
            else:
                auth_url = remote_url
                
            # Create temporary remote to avoid storing token permanently
            try:
                self.repo.delete_remote('documind_auth')
            except git.exc.GitCommandError:
                pass
                
            auth_remote = self.repo.create_remote('documind_auth', auth_url)
            auth_remote.push(branch_name)
            
            # Clean up the remote
            self.repo.delete_remote('documind_auth')
            
            print(f"🐙 Opening Pull Request on {repo_full_name}...")
            g = Github(self.github_token)
            gh_repo = g.get_repo(repo_full_name)
            
            pr = gh_repo.create_pull(
                title=title,
                body=body,
                head=branch_name,
                base="main" # Assuming base branch is main
            )
            print(f"✅ Pull Request Created Successfully! URL: {pr.html_url}")
            return True
            
        except Exception as e:
            print(f"⚠️ Failed to push or create PR: {e}")
            return False
