import chromadb
import os

class RepositoryMemory:
    def __init__(self, persist_dir="./.documind_db"):
        print("🧠 Initializing Repository Memory (ChromaDB)...")
        # Initialize an on-disk ChromaDB client
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(name="codebase_memory")
        
    def embed_file(self, file_path, content):
        """Embed a file's content into the vector DB for semantic search."""
        if not content.strip():
            return
            
        # MVP Chunking: Split by 1000 characters
        chunk_size = 1000
        chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
        
        ids = [f"{os.path.basename(file_path)}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [{"file": file_path} for _ in chunks]
        
        try:
            # Overwrite if exists to handle updates
            # In a full app, we would only upsert modified diffs
            self.collection.upsert(
                documents=chunks,
                metadatas=metadatas,
                ids=ids
            )
            print(f"✅ Embedded: {os.path.basename(file_path)}")
        except Exception as e:
            print(f"⚠️ Failed to embed {os.path.basename(file_path)}: {e}")
            
    def semantic_search(self, query, n_results=3):
        """Search the codebase for semantic matches to provide context to the LLM."""
        print(f"🔍 Searching memory for: '{query}'")
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            return results['documents'][0] if results['documents'] else []
        except Exception as e:
            print(f"⚠️ Search failed: {e}")
            return []
