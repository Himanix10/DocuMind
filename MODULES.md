# Module Level Documentation

This document explains the core modules and files within the **India Restaurant Finder** repository.

## `app.py`
**Purpose**: The main entry point for the Streamlit web application.
- **Initialization**: Configures the Streamlit page layout and custom CSS for aesthetics.
- **RAG Engine Initialization**: Defines `@st.cache_resource def init_rag()` to ensure the RAG engine (which loads embedding models and indexes data) is only instantiated once per session/server run.
- **Sidebar Navigation**: Renders the sidebar with predefined example queries, coverage info, and tech stack details. Example queries directly populate the session state.
- **Chat Interface**: Initializes `st.session_state.messages` to track conversation history.
- **Execution Loop**: Captures user input via `st.chat_input`, sends the query to the `rag.query()` method, streams the response utilizing a simulated typing effect (`time.sleep(0.02)`), and appends it to the chat history.

## `rag_engine.py`
**Purpose**: Encapsulates the Retrieval-Augmented Generation logic.

### Class: `RAGEngine`
- `__init__()`: Initializes the Groq LLM client, Azure Cognitive Search client, and SentenceTransformer model (`all-MiniLM-L6-v2`). Automatically triggers `_load_and_index_data()` upon instantiation.
- `_load_google_sheet_data()`: Uses `gspread` and `oauth2client` to authenticate and fetch the live dataset from a Google Sheet. Converts the response into a Pandas DataFrame.
- `_load_and_index_data()`: Iterates through the DataFrame, constructs a descriptive text block for each restaurant, generates an embedding vector, and maps the record to the Azure Search schema. Uploads the documents to Azure via `search_client.upload_documents`.
- `query(user_query: str) -> str`: 
  1. Vectorizes the `user_query`.
  2. Constructs a `VectorizedQuery` object targeting the `contentVector` field.
  3. Executes a hybrid search against Azure Cognitive Search (`search_text=user_query` + `vector_queries=[vector_query]`), requesting the top 5 results.
  4. Concatenates the retrieved documents into a context block.
  5. Passes the context and user query to Groq (`llama-3.3-70b-versatile`) with a predefined `system_prompt` instructing it to act as a warm local services assistant.
  6. Returns the LLM response string.

## `prepare_data.py`
**Purpose**: Ingests, cleans, and uploads the raw Swiggy dataset to Google Sheets.
- `prepare_swiggy_data()`: Reads `swiggy_file.csv` using Pandas. It handles missing columns by checking for multiple possible names (e.g., `city`, `Location`, `Area`). It sorts the data by rating (descending), handles missing values, and builds a standardized DataFrame with columns: `City`, `Name`, `Category`, `Area`, `Description`, `Rating`, `Phone`, `Price`, and `Google_Maps_Link`.
- `upload_to_google_sheets(df)`: Authenticates using a service account (`credentials.json`), connects to the target Google Sheet (`1lSobLES_B61sjYOl3Ko32ig_nktMtocmg7Ksvgl-dL4`), clears existing contents, and pushes the cleaned DataFrame.

## `setup_azure_index.py`
**Purpose**: Defines the Azure Search Index schema and provisions the index.
- `create_search_index()`: 
  1. Retrieves Azure endpoint and key from environment variables.
  2. Defines the fields schema using `SimpleField` and `SearchableField`.
  3. Specifies a `SearchField` named `contentVector` of type `Collection(Edm.Single)` with `vector_search_dimensions=384` (matching the `SentenceTransformer` output).
  4. Configures `VectorSearch` with `HnswAlgorithmConfiguration`.
  5. Uses `SearchIndexClient.create_or_update_index()` to provision the index on Azure.

## Configuration Files
- `.env`: (Not committed) Stores API keys and endpoints (`AZURE_SEARCH_ENDPOINT`, `AZURE_SEARCH_KEY`, `GROQ_API_KEY`, `GOOGLE_SHEET_ID`, `GOOGLE_CREDENTIALS_PATH`).
- `requirements.txt`: Python package dependencies (Streamlit, Groq, Azure SDKs, Pandas, SentenceTransformers, etc.).
