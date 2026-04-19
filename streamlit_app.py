__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
from src.phase_3_2_retrieval.rag_chain import answer_query, setup_rag_chain

st.set_page_config(
    page_title="HDFC AMC Stitch AI",
    page_icon="💼",
    layout="centered",
)

st.title("HDFC AMC Stitch AI 💼")
st.caption("Your personalized Mutual Fund Investment Assistant powered by RAG.")

# Initialize the RAG components in session state so it's loaded once
@st.cache_resource
def load_rag_components():
    with st.spinner("Connecting to Chroma Cloud..."):
        return setup_rag_chain()

rag_components = load_rag_components()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm Stitch, your HDFC investment expert. How can I help you grow your wealth today?"}
    ]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask Stitch anything about HDFC Mutual Funds..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response_data = answer_query(prompt, components=rag_components)
                response_text = response_data.get("result", "I'm sorry, I couldn't find an answer to that.")
            except Exception as e:
                response_text = f"An error occurred while fetching the answer: {str(e)}"
            
            st.markdown(response_text)
            
            # Optionally display source documents in an expander
            if "source_documents" in response_data and response_data["source_documents"]:
                with st.expander("View Source Context"):
                    for i, doc in enumerate(response_data["source_documents"]):
                        st.write(f"**Source {i+1}: {doc.metadata.get('title', 'Unknown')}**")
                        st.write(f"NAV: ₹{doc.metadata.get('nav', 'N/A')}")
                        st.text(doc.page_content)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_text})
