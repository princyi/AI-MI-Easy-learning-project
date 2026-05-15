"""
Code Interpreter Agent — Core Logic
--------------------------------------
This agent can answer data questions about a CSV file by:
1. Writing Python/Pandas code
2. Running it against the DataFrame
3. Returning the result

It uses LangChain's PythonREPLTool — a tool that executes Python code.
The agent thinks step-by-step (ReAct pattern): Thought → Action → Observation → Answer.
"""

import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_experimental.tools import PythonREPLTool
from langchain_experimental.utilities import PythonREPL
from langchain.agents import initialize_agent, AgentType
from langchain_core.messages import SystemMessage


def build_agent(csv_path: str):
    """
    Load the CSV into a DataFrame and create an agent that can query it with Python code.
    Returns a LangChain agent ready to answer questions.
    """
    # --- Step 1: Load CSV into a DataFrame ---
    df = pd.read_csv(csv_path)

    # --- Step 2: Create PythonREPLTool with df injected ---
    # PythonREPL is the underlying executor. We pass `df` and `pd` into its
    # `locals` dict so that any code the agent writes can reference them directly.
    repl = PythonREPL(_locals={"df": df, "pd": pd})
    python_tool = PythonREPLTool(python_repl=repl)

    # --- Step 3: Safety system message ---
    # We tell the agent what it's allowed to do (and what NOT to do).
    safety_note = SystemMessage(
        content=(
            "You are a data analyst. You have access to a DataFrame called `df`. "
            "Only use `df` and the pandas library to answer questions. "
            "Do NOT access the filesystem, run shell commands, or import unsafe modules. "
            "Always print your final answer using print()."
        )
    )

    # --- Step 4: Create the agent ---
    # ZERO_SHOT_REACT_DESCRIPTION = the agent reasons step-by-step without prior examples
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    agent = initialize_agent(
        tools=[python_tool],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        agent_kwargs={"system_message": safety_note},
        verbose=True,  # prints the agent's reasoning steps to the terminal
        handle_parsing_errors=True,
    )

    return agent


def run_query(agent, question: str) -> str:
    """
    Ask the agent a question about the DataFrame.
    Returns the agent's final answer as a string.
    """
    # .invoke() runs the full agent loop: think → write code → run code → answer
    result = agent.invoke({"input": question})
    return result["output"]
