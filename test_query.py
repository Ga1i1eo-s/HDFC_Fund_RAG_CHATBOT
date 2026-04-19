import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from src.phase_3_2_retrieval.rag_chain import answer_query

query = "What is the NAV and expense ratio of the HDFC Small Cap Fund? And what is the fund size?"
print(f"Question: {query}")
print("Thinking...")
response = answer_query(query)
print("\nAnswer:")
print(response['result'])
