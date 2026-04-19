import os
import logging
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import chromadb
from dotenv import load_dotenv

load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Instrument LangChain for Phoenix tracing (Phase 4)
try:
    from openinference.instrumentation.langchain import LangChainInstrumentor
    LangChainInstrumentor().instrument()
    logger.info("Arize Phoenix LangChain Instrumentation enabled.")
except ImportError:
    logger.info("Phoenix instrumentation skipped (module not found).")

def setup_rag_chain():
    """Initializes the Vector DB retriever (Pure Retrieval Mode via Chroma Cloud)."""
    
    # 1. Load Vector Database
    logger.info("Connecting to Chroma Cloud...")
        
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    
    chroma_client = chromadb.HttpClient(
        host="api.trychroma.com",
        ssl=True,
        headers={"x-chroma-token": os.environ.get("CHROMA_CLOUD_API_KEY", "")},
        tenant=os.environ.get("CHROMA_TENANT", "default_tenant"),
        database=os.environ.get("CHROMA_DATABASE", "default_database")
    )
    
    vectorstore = Chroma(
        client=chroma_client,
        collection_name="hdfc_mutual_funds",
        embedding_function=embeddings
    )
    
    # 2. Setup Retriever
    # Fetch only the single most relevant chunk for an exact answer
    retriever = vectorstore.as_retriever(search_kwargs={"k": 1})
    
    return {"retriever": retriever}

def answer_query(query, components=None):
    """Retrieves relevant context for a query using pure retrieval."""
    if not components:
        components = setup_rag_chain()
        
    logger.info(f"Retrieving chunks for query: {query}")
    
    # 1. Retrieve
    docs = components["retriever"].invoke(query)
    
    # 2. Format output
    if not docs:
        return {"result": "No relevant information found in the database.", "source_documents": docs}
        
    result_text = "Here are the most relevant extracts found in the database:\n\n"
    
    # Group by fund title to avoid duplicate headers
    funds_seen = set()
    
    for i, doc in enumerate(docs, 1):
        title = doc.metadata.get('title', 'Unknown')
        
        # Only print the big metadata header once per fund
        if title not in funds_seen:
            result_text += f"--- {title} ---\n"
            if 'nav' in doc.metadata:
                result_text += f"NAV: ₹{doc.metadata.get('nav')} | Expense Ratio: {doc.metadata.get('expense_ratio_percent')}% | Fund Size: ₹{doc.metadata.get('fund_size_cr')} Cr\n"
            else:
                result_text += "Metrics not found in metadata for this chunk.\n"
            
            result_text += "\n"
            funds_seen.add(title)
            
    return {
        "result": result_text.strip(),
        "source_documents": docs
    }

if __name__ == "__main__":
    chain = setup_rag_chain()
    print("Pure Retrieval System successfully initialized!")
