"""
Chatbot with Memory — Streamlit UI
-------------------------------------
A chat interface with a toggle to switch between two memory modes:
- Buffer Memory (remembers everything verbatim)
- Summary Memory (compresses old messages into a short summary)
"""

import streamlit as st
from chatbot import get_buffer_chain, get_summary_chain, chat

st.set_page_config(page_title="🧠 Memory Chatbot", page_icon="🧠")

st.title("🧠 Chatbot with Memory")
st.write("Chat with an AI that actually remembers what you said!")

# --- Memory mode selector ---
memory_mode = st.radio(
    "Choose memory type:",
    ["Buffer (remembers everything)", "Summary (compresses history)"],
    horizontal=True,
)

# --- Reset chat when the user switches memory mode ---
# We store the current mode in session_state to detect changes.
if "current_mode" not in st.session_state:
    st.session_state.current_mode = memory_mode

if st.session_state.current_mode != memory_mode:
    # Mode changed — clear history and rebuild the chain
    st.session_state.current_mode = memory_mode
    st.session_state.chain = None
    st.session_state.chat_history = []
    st.info("🔄 Memory mode changed — chat history cleared.")

# --- Initialise session state on first run ---
if "chain" not in st.session_state or st.session_state.chain is None:
    if "Buffer" in memory_mode:
        st.session_state.chain = get_buffer_chain()
    else:
        st.session_state.chain = get_summary_chain()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # list of {"role": "user"/"assistant", "content": "..."}

# --- Display chat history ---
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --- Chat input at the bottom ---
user_input = st.chat_input("Type a message...")

if user_input:
    # Show user message immediately
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Get assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = chat(st.session_state.chain, user_input)
        st.write(reply)

    # Save assistant reply to history
    st.session_state.chat_history.append({"role": "assistant", "content": reply})

# --- Show current memory contents in an expander ---
with st.expander("🔍 View memory"):
    memory = st.session_state.chain.memory
    if "Buffer" in memory_mode:
        # Buffer memory stores a list of messages
        messages = memory.chat_memory.messages
        if messages:
            for msg in messages:
                st.write(f"**{msg.type}:** {msg.content}")
        else:
            st.write("Memory is empty — start chatting!")
    else:
        # Summary memory stores a text summary
        summary = memory.moving_summary_buffer
        st.write(summary if summary else "No summary yet — start chatting!")
