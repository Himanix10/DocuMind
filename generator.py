import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class DocGenerator:
    def __init__(self):
        print("🤖 Initializing DocuMind Generator (Groq)...")
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("⚠️ GROQ_API_KEY not found in environment! Generation will fail.")
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"
        
    def generate_readme(self, repo_structure, file_contents):
        """Generates a comprehensive README.md based on repo contents."""
        print("📝 Generating README.md via LLM...")
        
        prompt = f"""
        You are DocuMind AI, an autonomous documentation agent.
        Based on the following repository structure and file contents, generate a comprehensive, 
        production-ready README.md. Include a Project Overview, Architecture, Tech Stack, and Setup Instructions.
        
        Repository Structure:
        {repo_structure}
        
        Key File Contents:
        {file_contents}
        
        Output ONLY raw Markdown. Do not include introductory text like 'Here is the markdown'.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert technical writer and software architect."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=4000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"⚠️ Failed to generate README: {e}")
            return "# Generated Documentation Failed\n\nEnsure GROQ_API_KEY is valid."
            
    def generate_api_specs(self, ast_data):
        """Generates an MODULES.md or API_SPECS.md based on extracted AST data."""
        print("📝 Generating MODULES.md via LLM...")
        
        prompt = f"""
        You are DocuMind AI. Create a clean, well-structured MODULES.md document based on the 
        extracted Abstract Syntax Tree (AST) data below. Document the purpose of the classes and functions.
        
        AST Data (Functions and Classes extracted from code):
        {ast_data}
        
        Output ONLY raw Markdown.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert API documentation writer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=4000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"⚠️ Failed to generate Modules Doc: {e}")
            return "# Modules Generation Failed"
