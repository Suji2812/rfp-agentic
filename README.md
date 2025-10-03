# RFP Agentic Demo (Hackathon starter)

## What
Prototype: Agentic AI for automating RFP response (Sales -> Technical -> Pricing -> Report).
Built with Python + Streamlit. Uses mock data.

## Run locally
1. python -m venv venv
2. source venv/bin/activate   # (Windows: venv\Scripts\activate)
3. pip install -r requirements.txt
4. streamlit run app.py

## Files
- agents/: agent implementations & orchestrator
- utils/: spec matching utilities
- data/: mock RFPs, product datasheets, pricing
- app.py: simple Streamlit UI to demo the pipeline

## Extend
- Use OpenAI or LangChain to parse free-text RFPs.
- Use a vector DB (FAISS/Pinecone) for product lookup.
- Integrate real tender portals / web scraping (careful with rate limits).
