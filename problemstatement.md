# Problem Statement: Mutual Fund RAG System

## Objective
To build a Retrieval-Augmented Generation (RAG) system that can answer user queries regarding specific mutual funds by extracting and referencing the latest data from IndMoney.

## Scope
The system will focus on the following 5 HDFC Mutual Funds:
1. HDFC Housing Opportunities Fund
2. HDFC Mid-Cap Opportunities Fund
3. HDFC Focused 30 Fund
4. HDFC Flexi Cap Fund
5. HDFC Small Cap Fund

## Key Data Points Required
For each of the mutual funds, the system MUST accurately extract and store the following key metrics:
- **NAV (Net Asset Value)**
- **Minimum SIP Amount**
- **Fund Size (AUM - Assets Under Management)**
- **Expense Ratio**
- **Rating (INDmoney Ranking / Peer Comparison)**

## Data Storage Strategy
To support accurate RAG queries, the data will be stored using a hybrid approach:
1. **Data Storage:** The text chunks and their embeddings will be stored in **Chroma Cloud** (trychroma.com). The HuggingFace `BAAI/bge-small-en-v1.5` embeddings model will be used for vectorization.
2. **Metadata / Structured Storage:** The key metrics (NAV, Min SIP, Fund Size, Expense Ratio, Rating) will be stored as structured metadata alongside the vector chunks (or in a separate lightweight SQL/JSON database). This allows the LLM to perform exact filtering (e.g., "Show funds with Expense Ratio < 1%") and retrieve exact numerical values without hallucination.
