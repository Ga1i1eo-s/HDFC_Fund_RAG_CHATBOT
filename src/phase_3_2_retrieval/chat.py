import sys
from rag_chain import setup_rag_chain, answer_query

def main():
    print("==================================================")
    print("   Mutual Fund RAG System - Chat Interface")
    print("==================================================")
    print("Initializing system... Please wait.")
    
    try:
        qa_chain = setup_rag_chain()
    except Exception as e:
        print(f"\n[ERROR] Failed to initialize RAG chain: {e}")
        print("Please ensure your .env file is set up with GROQ_API_KEY and the vector database is built.")
        sys.exit(1)
        
    print("\nSystem ready! Type 'exit' or 'quit' to stop.")
    print("--------------------------------------------------")
    
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.strip().lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
                
            if not user_input.strip():
                continue
                
            print("\nThinking...")
            response = answer_query(user_input, qa_chain)
            
            print("\nBot:", response['result'])
            
            # Optional: Print sources if needed
            # print("\n--- Sources ---")
            # for doc in response['source_documents']:
            #     print(f"- {doc.metadata.get('title', 'Unknown')} ({doc.metadata.get('source', '')})")
            # print("---------------")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\n[ERROR] An error occurred: {e}")

if __name__ == "__main__":
    main()
