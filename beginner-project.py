# Beginner Project Builder

A skill for creating beginner-friendly project scaffolding with heavy comments, simple layout, and a friendly README.

## Activation

Use this skill when the user asks to:
- Create a beginner project / starter project
- Scaffold a new project for learning
- Set up a simple project with explanations
- Build something for beginners or newcomers

## Instructions

When this skill is invoked, guide the agent to create a project that follows these strict principles:

### 🎯 Core Principles

1. **Keep it simple** — No complex patterns, no over-engineering. One file does one thing.
2. **Comment everything** — Every function, every variable, every block of logic must have a comment explaining *what* it does and *why*.
3. **Flat layout** — Avoid deep nesting of folders. Keep structure shallow and easy to navigate.
4. **Friendly README** — Always generate a README.md with emojis, clear sections, and step-by-step instructions.

---

### 📁 Project Layout

Use this flat, simple folder structure (adapt as needed for the language/framework):

```
project-name/
├── README.md          # Project overview and instructions
├── main.<ext>         # Entry point — where the program starts
├── helpers.<ext>      # Optional: utility/helper functions
├── config.<ext>       # Optional: configuration values
└── requirements.txt   # (Python) or package.json (Node) — dependencies
```

Avoid:
- More than 2 levels of nesting
- Separate `src/`, `lib/`, `utils/` folders unless absolutely necessary
- Abstract base classes, factories, or design patterns

---

### 🗒️ Code Style Rules

Apply these to every file created:

**Header comment** at the top of every file:
```python
# ============================================================
# File: main.py
# Purpose: Entry point for the app — this is where it all starts
# ============================================================
```

**Function comments** before every function:
```python
# This function greets the user by name
# Parameters:
#   name (str): The person's name
# Returns:
#   str: A friendly greeting message
def greet(name):
    ...
```

**Inline comments** on non-obvious lines:
```python
result = value * 1.18  # Multiply by 1.18 to add 18% GST tax
```

**Section dividers** to group related code:
```python
# ---- Setup ----
# ---- Main Logic ----
# ---- Output ----
```

---

### 📄 README Template

Always generate a `README.md` using this structure with emojis:

```markdown
# 🚀 <Project Name>

> One-line description of what this project does.

---

## 📖 What is this?

A short paragraph (2-3 sentences) explaining what the project does, in plain language.
No jargon. Write as if explaining to someone who just started coding.

---

## 🗂️ Project Structure

```
project-name/
├── README.md     → You are here!
├── main.py       → Start here — runs the app
├── helpers.py    → Helper functions used by main.py
```

---

## ⚙️ How to Run

Step-by-step instructions:

1. **Install Python** (if not already): [python.org](https://python.org)
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the app**:
   ```bash
   python main.py
   ```

---

## 🧠 How it Works

Brief explanation of the key idea behind the code.
Link concepts to beginner-friendly resources where possible.

---

## 🛠️ Tech Used

- **Python 3.x** — main language
- **[Library Name]** — what it's used for

---

## 🙋 Questions?

If you're stuck, try:
- Reading the comments in each file — they explain everything!
- Searching on [Stack Overflow](https://stackoverflow.com)
- Asking GitHub Copilot in your editor 😊
```

---

### ✅ Checklist Before Finishing

Before completing the scaffolding, verify:

- [ ] Every file has a header comment
- [ ] Every function has a docstring or block comment
- [ ] No file is longer than ~100 lines (split if needed)
- [ ] Folder depth is max 2 levels
- [ ] README.md exists with emojis and run instructions
- [ ] Dependencies file exists (requirements.txt / package.json)
- [ ] No unexplained "magic" values — use named constants with comments

---

### 💬 Tone for Comments

Write comments as if you're a friendly senior developer explaining to a junior:
- "This sets up our database connection — think of it like opening a phone book"
- "We use a list here because we need to store multiple items in order"
- "This loop goes through each item one by one and processes it"

Avoid terse comments like `# increment i` or `# call function`.
