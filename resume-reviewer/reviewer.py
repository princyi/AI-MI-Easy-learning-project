"""
Resume Reviewer — Core Logic
------------------------------
This file:
1. Extracts text from a PDF resume using PyPDF2
2. Sends it to GPT-3.5 with a recruiter persona
3. Returns structured feedback (score, strengths, improvements, rewrite tip)
"""

import PyPDF2
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException
from langchain_core.prompts import PromptTemplate


# --- Step 1: Define the feedback schema ---
# Pydantic ensures the LLM always returns these exact fields in the right types.
class ResumeFeedback(BaseModel):
    score: int                  # Overall score out of 10
    strengths: list[str]        # Things the resume does well
    improvements: list[str]     # Specific areas to fix
    rewrite_tip: str            # One concrete rewrite suggestion


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Read all pages from a PDF file and return the combined text as a string.
    Uses PyPDF2 — works for text-based PDFs (not scanned images).
    """
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        # Loop through every page and extract its text
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:  # some pages may be blank/unreadable
                text += page_text + "\n"
    return text.strip()


def review_resume(pdf_path: str) -> ResumeFeedback:
    """
    Extract text from a PDF resume, send it to GPT, and return structured feedback.
    """
    # --- Step 2: Extract text ---
    resume_text = extract_text_from_pdf(pdf_path)
    if not resume_text:
        raise ValueError("Could not extract text from this PDF. It may be a scanned image.")

    # --- Step 3: Set up parser + prompt ---
    parser = PydanticOutputParser(pydantic_object=ResumeFeedback)
    format_instructions = parser.get_format_instructions()

    # The prompt asks the LLM to act as a senior recruiter
    prompt = PromptTemplate(
        input_variables=["resume_text"],
        partial_variables={"format_instructions": format_instructions},
        template=(
            "You are a senior technical recruiter. Evaluate the resume below for:\n"
            "- Clarity and readability\n"
            "- Impact (does it show achievements, not just duties?)\n"
            "- ATS compatibility (keywords, formatting)\n\n"
            "Resume:\n{resume_text}\n\n"
            "Provide your feedback as JSON following this schema:\n"
            "{format_instructions}"
        ),
    )

    # --- Step 4: Call the LLM with retry for parse failures ---
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    formatted_prompt = prompt.format(resume_text=resume_text[:6000])  # guard against token limit

    last_error = None
    for attempt in range(1, 4):  # up to 3 attempts
        try:
            response = llm.invoke(formatted_prompt)
            feedback = parser.parse(response.content)
            return feedback
        except OutputParserException as e:
            last_error = e
            print(f"Parse attempt {attempt} failed: {e}")

    raise last_error
