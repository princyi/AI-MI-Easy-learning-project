# 📊 Project 04 — Code Interpreter Agent

> **The Big Idea:** Instead of writing Pandas code yourself, describe what you want in plain English and let the AI write and run the code for you!

---

## 🤔 What does this app do?

1. You upload a **CSV file** (any dataset)
2. The app shows you a preview of the data
3. You ask a question like *"What is the average salary?"* or *"Which city has the most customers?"*
4. An **AI agent** thinks step-by-step, writes Python/Pandas code, runs it, and returns the answer

---

## 🧠 Concepts you'll learn

| Concept | What it means |
|---|---|
| **AI Agent** | An LLM that can use tools (not just answer questions) |
| **PythonREPLTool** | A tool that lets the agent execute real Python code |
| **ReAct Pattern** | Reason → Act → Observe → Repeat until done |
| **ZERO_SHOT_REACT_DESCRIPTION** | Agent that figures out what to do with no examples |
| **System message** | Instructions that constrain what the agent is allowed to do |

---

## 📁 Files

```
code-agent/
├── app.py      ← Streamlit UI (CSV upload + question + result display)
├── agent.py    ← LangChain agent with PythonREPLTool
└── requirements.txt
```

---

## 🚀 How to run

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
streamlit run app.py
```

---

## 🗺️ How the code flows

```
User uploads CSV
       ↓
agent.py: build_agent(csv_path)
   ├── Load CSV → pandas DataFrame (df)
   ├── Create PythonREPLTool with df in scope
   └── Initialize agent (ZERO_SHOT_REACT_DESCRIPTION)
       ↓
User asks a question
       ↓
agent.py: run_query(agent, question)
   └── Agent loop:
       ├── Thought: "I need to find the average of column X"
       ├── Action: Run `print(df['X'].mean())`
       ├── Observation: "42.5"
       └── Final Answer: "The average is 42.5"
       ↓
app.py shows the answer
```

---

## ⚠️ Safety Note

The `PythonREPLTool` runs **real Python code** on your machine. The system message restricts the agent to only use `df` and pandas, but you should:
- Only use this with trusted CSV files
- Never run this on a production server with sensitive data
- Review the agent's reasoning steps (visible in your terminal)

---

## 💡 Tips for beginners

- Try a simple CSV first — e.g. a spreadsheet exported from Excel
- The agent's step-by-step reasoning prints to your **terminal** (look there!)
- Good example questions: *"How many rows?"*, *"What are the column names?"*, *"Show me the top 5 by sales"*
