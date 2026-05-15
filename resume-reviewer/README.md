# 📝 Project 05 — Resume Reviewer

> Upload your PDF resume and get instant, structured feedback from an AI acting as a senior recruiter. No more guessing if your resume is ATS-friendly!

---

## 🤔 What does this app do?

1. You upload your **PDF resume**
2. PyPDF2 extracts the text from every page
3. The AI (acting as a senior recruiter) evaluates it for:
   - 📖 Clarity & readability
   - 🎯 Impact (achievements vs. just listing duties)
   - 🤖 ATS compatibility (keywords, formatting)
4. You get back a structured report: score, strengths, improvements, rewrite tip

---

## 🧠 Concepts you'll learn

| Concept | What it means |
|---|---|
| **PyPDF2** | Python library to extract text from PDF files |
| **Pydantic model** | Defines the exact shape of the AI's response |
| **PydanticOutputParser** | Parses the LLM's text output into a Python object |
| **Persona prompting** | Telling the LLM to act as a specific expert |
| **st.metric / st.success / st.warning** | Streamlit display components |

---

## 📁 Files

```
resume-reviewer/
├── app.py          ← Streamlit UI (PDF upload + feedback display)
├── reviewer.py     ← PDF extraction + prompt + LLM call
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
User uploads PDF
       ↓
reviewer.py: review_resume(pdf_path)
   ├── extract_text_from_pdf() → raw text string
   ├── Build PromptTemplate with resume text + format_instructions
   ├── Call ChatOpenAI
   └── Parse response → ResumeFeedback object
       ↓
app.py displays:
   ├── st.metric → score out of 10
   ├── st.success → each strength (green)
   ├── st.warning → each improvement (yellow)
   └── st.info → rewrite tip (blue)
```

---

## 💡 Tips for beginners

- Make sure your PDF is **text-based** (not a scanned image) — PyPDF2 can't read images
- Try uploading a simple 1-page resume first
- The `ResumeFeedback` Pydantic class in `reviewer.py` is the schema — try adding a new field!
- Experiment with the prompt: change the recruiter's focus (e.g. "evaluate for a software engineer role")
