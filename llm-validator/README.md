# 🎬 Project 02 — LLM Output Validator

> **The Problem:** LLMs are unpredictable — they might return a half-formed JSON, add extra commentary, or forget a required field.  
> **The Solution:** Use **Pydantic** to define the exact shape you want, and **retry** automatically if the output is invalid.

---

## 🤔 What does this app do?

1. You type a prompt like *"Review the movie Interstellar"*
2. The app sends it to GPT with strict formatting instructions
3. GPT returns a structured JSON with: title, rating, summary, pros, cons
4. Pydantic **validates** the response — if it's wrong, it retries (up to 3 times)
5. You see the result displayed in a clean, structured layout

---

## 🧠 Concepts you'll learn

| Concept | What it means |
|---|---|
| **Pydantic Model** | A Python class that defines and validates data types |
| **PydanticOutputParser** | Tells the LLM what JSON format to return |
| **format_instructions** | Auto-generated text injected into the prompt |
| **Retry logic** | Catch `OutputParserException` and try again |

---

## 📁 Files

```
llm-validator/
├── app.py           ← Streamlit UI (prompt input + structured display)
├── validator.py     ← Pydantic schema + LLM call + retry loop
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
User types a prompt
       ↓
validator.py: get_structured_review(prompt)
   ├── Build PromptTemplate with {format_instructions}
   ├── Send to ChatOpenAI
   ├── Try to parse response → MovieReview object
   └── If parsing fails → retry (max 3 times)
       ↓
app.py displays:
   ├── st.metric for title + rating
   ├── st.success for each pro
   └── st.warning for each con
```

---

## 💡 Tips for beginners

- Try typing *"Review a bad movie"* — the AI still has to give structured output!
- Open `validator.py` and look at the `MovieReview` class — that's your schema
- `format_instructions` is just a string that tells the LLM *"return JSON with these fields"*
- Pydantic's job is to **catch typos in the LLM's output** before your app crashes
