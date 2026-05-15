"""
LLM Output Validator — Core Logic
-----------------------------------
Problem: LLMs sometimes return messy or incomplete JSON.
Solution: Use Pydantic to define the exact shape we want, then retry if it's wrong.

Steps:
1. Define the schema (MovieReview Pydantic model)
2. Tell the LLM exactly what format to return using format_instructions
3. Parse the response; if it's bad, retry up to 3 times
"""

from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.exceptions import OutputParserException

# --- Step 1: Define the schema ---
# Pydantic models are like blueprints — they define what fields we expect and their types.
# If the LLM returns something that doesn't match, Pydantic will raise an error.
class MovieReview(BaseModel):
    title: str           # Name of the movie
    rating: int          # Score out of 10
    summary: str         # One-paragraph summary
    pros: list[str]      # List of good things
    cons: list[str]      # List of bad things


def get_structured_review(user_prompt: str) -> MovieReview:
    """
    Send a prompt to the LLM and return a validated MovieReview object.
    Retries up to 3 times if the output can't be parsed.
    """

    # --- Step 2: Set up the parser ---
    # PydanticOutputParser knows the MovieReview schema and can parse LLM text into it.
    parser = PydanticOutputParser(pydantic_object=MovieReview)

    # format_instructions tells the LLM exactly what JSON format to use.
    # Example output: "Return a JSON object with fields: title, rating, summary, pros, cons"
    format_instructions = parser.get_format_instructions()

    # --- Step 3: Build the prompt ---
    # {user_prompt} = what the user typed  (e.g. "Review the movie Inception")
    # {format_instructions} = exact JSON schema the LLM must follow
    prompt_template = PromptTemplate(
        input_variables=["user_prompt"],
        partial_variables={"format_instructions": format_instructions},
        template=(
            "You are a movie critic. {user_prompt}\n\n"
            "Respond ONLY with valid JSON following this schema:\n"
            "{format_instructions}"
        ),
    )

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    # --- Step 4: Retry loop ---
    last_error = None
    for attempt in range(1, 4):  # attempts 1, 2, 3
        try:
            # Format the prompt with the user's input
            formatted_prompt = prompt_template.format(user_prompt=user_prompt)

            # Send to LLM and get back a string response
            response = llm.invoke(formatted_prompt)

            # Try to parse the string into a MovieReview object
            # If the JSON is malformed, this raises OutputParserException
            review = parser.parse(response.content)
            return review  # Success! Return early.

        except OutputParserException as e:
            # Only retry on parse failures — not on network/auth errors
            last_error = e
            print(f"Attempt {attempt} failed to parse output: {e}")

    # If we reach here, all 3 attempts failed
    raise last_error
