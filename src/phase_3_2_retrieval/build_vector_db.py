import os
import json
import logging
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import chromadb
from dotenv import load_dotenv

load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DATA_DIR = os.path.join(BASE_DIR, 'data', 'raw')

def load_documents():
    """Load JSON files from the data directory into LangChain Documents."""
    documents = []
    if not os.path.exists(DATA_DIR):
        logger.error(f"Data directory {DATA_DIR} does not exist. Run Phase 3.1 scraper first.")
        return documents

    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(DATA_DIR, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Combine base data and specific metadata
                metadata = data.get("metadata", {})
                metadata["source"] = data.get("url", "")
                metadata["title"] = data.get("title", "")
                
                # We must ensure metadata values are simple types (str, int, float, bool)
                # Chroma doesn't like None values, so we filter them out
                clean_metadata = {k: v for k, v in metadata.items() if v is not None}
                
                doc = Document(
                    page_content=data.get("content", ""),
                    metadata=clean_metadata
                )
                documents.append(doc)
    
    logger.info(f"Loaded {len(documents)} documents from {DATA_DIR}")
    return documents

def build_vector_db():
    documents = load_documents()
    if not documents:
        return
        
    # Split text into chunks
    logger.info("Splitting text into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len
    )
    chunks = text_splitter.split_documents(documents)
    logger.info(f"Created {len(chunks)} chunks.")

    # Initialize Embeddings
    logger.info("Initializing HuggingFace Embeddings (BAAI/bge-small-en-v1.5)...")
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    
    # Connect to Chroma Cloud
    logger.info("Connecting to Chroma Cloud (trychroma.com)...")
    chroma_client = chromadb.HttpClient(
        host="api.trychroma.com",
        ssl=True,
        headers={"x-chroma-token": os.environ.get("CHROMA_CLOUD_API_KEY", "")},
        tenant=os.environ.get("CHROMA_TENANT", "default_tenant"),
        database=os.environ.get("CHROMA_DATABASE", "default_database")
    )

    # Create and persist the Vector Database remotely
    logger.info("Uploading chunks to Chroma Cloud...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        client=chroma_client,
        collection_name="hdfc_mutual_funds"
    )
    logger.info("Vector database successfully built and uploaded to Chroma Cloud!")

if __name__ == "__main__":
    build_vector_db()
