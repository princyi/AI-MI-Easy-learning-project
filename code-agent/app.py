"""
Code Interpreter Agent — Streamlit UI
----------------------------------------
Upload a CSV → ask data questions in plain English → get answers!
The AI writes Python code, runs it, and returns the result.
"""

import os
import tempfile
import streamlit as st
import pandas as pd
from agent import build_agent, run_query

st.set_page_config(page_title="📊 Data Agent", page_icon="📊")

st.title("📊 CSV Data Agent")
st.write("Upload a CSV file and ask questions about it in plain English.")

# Safety disclaimer — always good practice when running AI-generated code!
st.warning(
    "⚠️ **Note:** This app runs AI-generated Python code. "
    "Only use it with trusted data files in a controlled environment."
)

# --- CSV file uploader ---
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the CSV for the preview (doesn't need the agent yet)
    df_preview = pd.read_csv(uploaded_file)

    st.write("### 👀 Data Preview")
    st.dataframe(df_preview.head())  # show first 5 rows
    st.write(f"📐 Shape: {df_preview.shape[0]} rows × {df_preview.shape[1]} columns")

    # Build the agent only once per uploaded file
    if "agent" not in st.session_state or st.session_state.agent_file != uploaded_file.name:
        with st.spinner("🔧 Building data agent..."):
            # Save to a temp file so pandas can read it from disk
            with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
                uploaded_file.seek(0)  # rewind after the preview read
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            st.session_state.agent = build_agent(tmp_path)
            st.session_state.agent_file = uploaded_file.name
            os.unlink(tmp_path)  # clean up temp file

        st.success("✅ Agent ready!")

    # --- Question input ---
    question = st.text_input(
        "💬 Ask a question about your data",
        placeholder="e.g. What is the average age? Which city has the most orders?",
    )

    if question:
        with st.spinner("🤖 Agent is thinking and writing code..."):
            answer = run_query(st.session_state.agent, question)

        st.success(f"**Answer:** {answer}")

        # Show agent's step-by-step reasoning
        with st.expander("🔍 See agent reasoning"):
            st.write(
                "The agent's reasoning steps are printed in your **terminal** "
                "(because `verbose=True` in agent.py). "
                "Check the terminal window where you ran `streamlit run app.py`."
            )
