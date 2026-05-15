# 🧪 AI Engineering Lab for learning easy way Genai making prjects

> **5 beginner-friendly GenAI projects** built with Python, LangChain, and Streamlit.  
> Each project is self-contained in its own folder with a detailed README.

---

## 🚀 Quick Start

**1. Install all dependencies (one command)**
```bash
pip install openai langchain langchain-openai langchain-community langchain-experimental streamlit chromadb sentence-transformers pydantic pypdf2 pandas
```

**2. Set your OpenAI API key**
```bash
export OPENAI_API_KEY=sk-...
```

**3. Run any project**
```bash
cd <project-folder>
streamlit run app.py
```

---

## 📦 Projects

| # | Folder | What you build | Key concepts |
|---|---|---|---|
| 01 | [`rag-app/`](./rag-app/) | 📄 Upload a PDF/TXT and ask questions about it | RAG, ChromaDB, embeddings |
| 02 | [`llm-validator/`](./llm-validator/) | 🎬 Get structured movie reviews from the LLM | Pydantic, output parsing, retry |
| 03 | [`chatbot-memory/`](./chatbot-memory/) | 🧠 Chatbot that remembers your conversation | Buffer memory, summary memory |
| 04 | [`code-agent/`](./code-agent/) | 📊 Ask data questions about a CSV in plain English | Agents, PythonREPLTool, ReAct |
| 05 | [`resume-reviewer/`](./resume-reviewer/) | 📝 Get AI feedback on your PDF resume | PDF parsing, structured prompts |

---

## 📁 Project Structure

```
ai-engineering-lab/
├── rag-app/
│   ├── app.py           ← Streamlit UI
│   ├── rag.py           ← RAG logic
│   └── README.md
├── llm-validator/
│   ├── app.py
│   ├── validator.py
│   └── README.md
├── chatbot-memory/
│   ├── app.py
│   ├── chatbot.py
│   └── README.md
├── code-agent/
│   ├── app.py
│   ├── agent.py
│   └── README.md
└── resume-reviewer/
    ├── app.py
    ├── reviewer.py
    └── README.md
```

---

## 💡 Learning Path

1. Start with **Project 01** (RAG) to understand the basics of embeddings and document retrieval.  
2. Then try **Project 02** (Validator) to learn about structured outputs.  
3. Work through them in order — each one builds on concepts from the previous.

---

## 🔑 Rules followed in every project

- All API keys loaded from environment variables (`os.environ["OPENAI_API_KEY"]`)
- Uses `gpt-3.5-turbo` (cheap and fast — great for learning)/ uses ollam for free to get this all tools 
- Every non-obvious line has a comment explaining *why*
- Each file stays under 100 lines for easy reading
- `st.session_state` used to avoid expensive re-runs in Streamlit
