import os
import sys
import logging

# Add the root project directory to the python path so we can import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.phase_3_2_retrieval.rag_chain import answer_query

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# A "Golden Dataset" of test queries and the expected fund title
GOLDEN_DATASET = [
    {
        "query": "What is the NAV of HDFC Small Cap Fund?",
        "expected_fund": "HDFC Small Cap Fund"
    },
    {
        "query": "Tell me about HDFC Flexi Cap strategy",
        "expected_fund": "HDFC Flexi Cap Fund"
    },
    {
        "query": "Minimum SIP for Focused 30?",
        "expected_fund": "HDFC Focused 30 Fund"
    },
    {
        "query": "What is the expense ratio for HDFC Mid-Cap Opportunities?",
        "expected_fund": "HDFC Mid-Cap Opportunities Fund"
    },
    {
        "query": "Show me the AUM of Housing Opportunities fund",
        "expected_fund": "HDFC Housing Opportunities Fund"
    }
]

def evaluate_retrieval():
    logger.info("Starting Deterministic Retrieval Evaluation...")
    logger.info("---------------------------------------------")
    
    total_queries = len(GOLDEN_DATASET)
    successful_retrievals = 0
    
    for item in GOLDEN_DATASET:
        query = item["query"]
        expected = item["expected_fund"]
        
        logger.info(f"Query: '{query}'")
        logger.info(f"Expected: {expected}")
        
        # We only need the source_documents to evaluate retrieval
        response = answer_query(query)
        docs = response.get("source_documents", [])
        
        # Check if the expected fund appears in ANY of the top-k retrieved chunks
        found = False
        retrieved_funds = set()
        
        for doc in docs:
            title = doc.metadata.get("title", "")
            retrieved_funds.add(title)
            if expected.lower() in title.lower():
                found = True
                
        if found:
            logger.info("Status: [PASS] - Correct document was retrieved in the Top K results.")
            successful_retrievals += 1
        else:
            logger.info(f"Status: [FAIL] - Retrieved funds were: {list(retrieved_funds)}")
            
        logger.info("---------------------------------------------")
        
    accuracy = (successful_retrievals / total_queries) * 100
    logger.info(f"\nFinal Retrieval Accuracy: {accuracy:.2f}% ({successful_retrievals}/{total_queries})")

if __name__ == "__main__":
    evaluate_retrieval()
