# 🧠 Project 03 — Chatbot with Memory

> **The Problem:** By default, every LLM call is stateless — it forgets everything you said.  
> **The Solution:** LangChain's **memory** objects store the conversation and inject it into every new prompt.

---

## 🤔 What does this app do?

A chat interface where you can toggle between two memory modes:

| Mode | How it works | Best for |
|---|---|---|
| 🗂️ **Buffer** | Stores every message word-for-word | Short conversations |
| 📝 **Summary** | Compresses old messages into a summary | Long conversations |

---

## 🧠 Concepts you'll learn

| Concept | What it means |
|---|---|
| **ConversationChain** | A LangChain chain that remembers context |
| **ConversationBufferMemory** | Stores all messages verbatim |
| **ConversationSummaryMemory** | Summarises old messages to save tokens |
| **st.chat_message** | Streamlit's built-in chat bubble component |
| **st.session_state** | Keeps the chain alive across Streamlit reruns |

---

## 📁 Files

```
chatbot-memory/
├── app.py        ← Streamlit chat UI + memory mode toggle
├── chatbot.py    ← LangChain chains with both memory types
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
User picks memory mode (Buffer or Summary)
       ↓
chatbot.py creates a ConversationChain with the chosen memory
       ↓
User types a message
       ↓
chatbot.py: chat(chain, message)
   └── chain.predict(input=message)
       ├── Memory adds conversation history to the prompt
       ├── LLM generates a response
       └── Memory updates (saves new message or updates summary)
       ↓
app.py shows the reply + updates chat history
```

---

## 💡 Tips for beginners

- Switch memory modes mid-conversation to see how they differ
- Click **"View memory"** at the bottom to see what's stored inside each memory object
- Summary memory makes an *extra* LLM call to compress history — watch your token count!
- Try a long conversation (10+ messages) to really see the difference
