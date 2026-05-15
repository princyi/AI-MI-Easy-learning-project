"""
Chatbot with Memory — Core Logic
----------------------------------
Two types of memory in LangChain:

1. Buffer Memory   → stores every message verbatim
                    👍 Perfect recall  👎 Gets very long quickly

2. Summary Memory  → summarises old messages to save space
                    👍 Handles long conversations  👎 Might lose small details

This file builds both chains and exposes a simple chat() function.
"""

from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory  # noqa: these still work via langchain compat layer


def get_buffer_chain() -> ConversationChain:
    """
    Create a conversation chain that remembers EVERY message word-for-word.
    Good for short chats where you want nothing to be forgotten.
    """
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

    # ConversationBufferMemory appends each message to a running list
    memory = ConversationBufferMemory()

    # ConversationChain ties the LLM + memory together.
    # It automatically adds the conversation history to each prompt.
    return ConversationChain(llm=llm, memory=memory, verbose=False)


def get_summary_chain() -> ConversationChain:
    """
    Create a conversation chain that compresses old messages into a short summary.
    Good for long conversations — uses fewer tokens over time.
    """
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

    # ConversationSummaryMemory uses another LLM call to summarise history.
    # It needs an llm= argument because summarising is itself an LLM task.
    memory = ConversationSummaryMemory(llm=ChatOpenAI(model="gpt-3.5-turbo"))

    return ConversationChain(llm=llm, memory=memory, verbose=False)


def chat(chain: ConversationChain, user_message: str) -> str:
    """
    Send a message to the conversation chain and return the assistant's reply.
    The chain automatically updates its memory after each call.
    """
    # .predict() is the simplest way to get a string response from a ConversationChain
    response = chain.predict(input=user_message)
    return response
