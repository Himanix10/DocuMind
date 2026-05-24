# API Integration Specifications

The **India Restaurant Finder** application relies entirely on external managed services for its core processing. This document outlines the API integrations and their configuration parameters.

## 1. Groq LLM API
Handles the generation of conversational responses based on the retrieved context.

- **Endpoint**: `https://api.groq.com/openai/v1/chat/completions` (via Python `groq` package)
- **Model Used**: `llama-3.3-70b-versatile`
- **Authentication**: API Key loaded from `GROQ_API_KEY` in environment variables.

### Request Configuration (`rag_engine.py`)
```python
response = self.groq_client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Based on this information... {context}... User question: {user_query}"}
    ],
    temperature=0.7,
    max_tokens=600
)
```
- **Temperature (0.7)**: Set to provide a balance between creativity and accuracy, making the response sound conversational but strictly grounded.
- **Max Tokens (600)**: Limits the response length to keep outputs concise and cost-effective.

## 2. Azure Cognitive Search API
Provides vector storage and hybrid search capabilities.

- **Service**: Azure Cognitive Search Resource
- **Authentication**: `AzureKeyCredential` using `AZURE_SEARCH_KEY` and `AZURE_SEARCH_ENDPOINT`.
- **Index Name**: `india-services-index`
- **Vector Algorithm**: HNSW (Hierarchical Navigable Small World)
- **Embedding Dimensions**: `384`

### Hybrid Search Implementation (`rag_engine.py`)
The search queries both the full-text and the vector dimensions simultaneously.
```python
vector_query = VectorizedQuery(
    vector=query_vector,          # 384-dimensional float array
    k_nearest_neighbors=5,        # Retrieve top 5 closest vectors
    fields="contentVector"        # Target field in Azure schema
)

results = self.search_client.search(
    search_text=user_query,       # Keyword search component
    vector_queries=[vector_query],# Vector search component
    select=["name", "content", "city", "rating", "phone", "area", "price"],
    top=5                         # Final top K documents returned
)
```

## 3. Google Sheets API
Serves as the dynamic data store for the application.

- **Authentication**: OAuth2 Service Account Credentials JSON (`GOOGLE_CREDENTIALS_PATH`).
- **Scopes**: `https://spreadsheets.google.com/feeds`, `https://www.googleapis.com/auth/drive`
- **Library**: `gspread` & `oauth2client`

### Operations
- **Data Ingestion (`prepare_data.py`)**: Connects to `GOOGLE_SHEET_ID`, clears the existing `sheet1`, and uploads a 2D array representing the DataFrame.
- **Data Fetching (`rag_engine.py`)**: Connects to `GOOGLE_SHEET_ID` and executes `sheet.get_all_records()` to retrieve data into a List of Dictionaries for vectorization on application startup.
