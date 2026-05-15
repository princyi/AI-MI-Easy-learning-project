"""
Resume Reviewer — Streamlit UI
---------------------------------
Upload your PDF resume and get structured AI feedback instantly.
"""

import os
import tempfile
import streamlit as st
from reviewer import review_resume

st.set_page_config(page_title="📝 Resume Reviewer", page_icon="📝")

st.title("📝 AI Resume Reviewer")
st.write("Upload your resume (PDF) and get feedback from an AI recruiter in seconds!")

# --- PDF uploader ---
uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])

if uploaded_file is not None:
    if st.button("🔍 Review My Resume"):
        with st.spinner("📖 Reading your resume and asking the AI recruiter..."):
            # Save uploaded PDF to a temp file so reviewer.py can open it
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            try:
                feedback = review_resume(tmp_path)
            except Exception as e:
                st.error(f"❌ Could not process the resume: {e}")
                st.stop()  # halt this rerun — don't try to display feedback below
            finally:
                # Always clean up the temp file, even if an error occurred
                os.unlink(tmp_path)

        # --- Display results ---
        st.write("---")

        # Overall score — big metric display
        st.metric("⭐ Overall Score", f"{feedback.score} / 10")

        # Strengths — green boxes
        st.write("### ✅ Strengths")
        for strength in feedback.strengths:
            st.success(f"👍 {strength}")

        # Improvements — yellow warnings
        st.write("### 🔧 Areas to Improve")
        for improvement in feedback.improvements:
            st.warning(f"💡 {improvement}")

        # Rewrite tip — blue info box
        st.write("### ✍️ Rewrite Tip")
        st.info(feedback.rewrite_tip)
