
# 📊 Multi-Source Analyst Agent

This project is an intelligent question-answering system powered by Streamlit and LangChain agents. It enables users to upload CSVs or PDFs, search the web, and ask natural language questions — getting insightful answers with sources cited.

---

## 🚀 Features

- 📁 Upload CSV or PDF files (stored locally)
- 🌐 Optional Web Search using Tavily API
- 🤖 LangGraph-based multi-agent pipeline:
  - SQL Agent
  - RAG Agent (PDFs)
  - Web Search Agent
  - Summarizer Agent
- 📜 Conversational UI with history
- 📥 Export response to PDF
- 🌈 Stylish UI with Accenture-like purple theme

---

## 🧠 Project Structure

```bash
.
├── app.py                      # Streamlit frontend
├── requirements.txt
├── assets/
│   └── style.css              # Custom Streamlit CSS
├── src/
│   ├── clients/
│   │   └── openai.py          # OpenAI client (Chat + Embeddings)
│   ├── data/
│   │   ├── docs/              # Uploaded PDFs
│   │   └── sheets/            # Uploaded CSVs
│   ├── agents/
│   │   ├── rag_agent.py       # RAG over PDFs
│   │   ├── sql_agent.py       # SQL reasoning
│   │   ├── summarize_agent.py # Summarizer over sources
│   │   └── web_search_agent.py# Web search via Tavily
│   └── utils/
│       ├── pdf_loader.py      # PDF text splitting, FAISS indexing
│       └── embedder.py        # OpenAI Embeddings wrapper
```

---

## ⚙️ Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/multi-source-analyst-agent.git
cd multi-source-analyst-agent
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Add `.env` file with your API keys**
```env
OPENAI_API_KEY=your_openai_key
TAVILY_API_KEY=your_tavily_key
```

---

## ▶️ Running the App

```bash
streamlit run app.py
```

Upload PDFs/CSVs, type your question, and get responses with sources!

---

## 📌 Notes

- FAISS is used locally (no vector DB needed).
- SQL queries run via `duckdb`, data loaded from uploaded CSVs.
- Web search uses [Tavily API](https://app.tavily.com/).
- PDF export uses `fpdf`.

---


