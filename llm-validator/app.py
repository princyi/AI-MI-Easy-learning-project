"""
LLM Output Validator — Streamlit UI
-------------------------------------
This app shows how to get structured, reliable output from an LLM.
The user types a prompt; we always get back a clean MovieReview object.
"""

import streamlit as st
from validator import get_structured_review, MovieReview

st.set_page_config(page_title="🎬 Movie Review AI", page_icon="🎬")

st.title("🎬 Movie Review AI")
st.write("Ask for a review of any movie. The AI will return a structured response every time.")

# --- User input ---
user_prompt = st.text_area(
    "Your prompt",
    placeholder='e.g. "Review the movie Inception"',
    height=100,
)

if st.button("🎬 Get Review"):
    if not user_prompt.strip():
        st.error("Please enter a prompt first.")
    else:
        with st.spinner("🤖 Asking the AI..."):
            try:
                review = get_structured_review(user_prompt)
                st.success("✅ Got a valid structured response!")

                # --- Display the structured fields ---
                col1, col2 = st.columns(2)
                with col1:
                    # st.metric shows a number with a label — great for scores
                    st.metric("🎬 Movie", review.title)
                with col2:
                    st.metric("⭐ Rating", f"{review.rating} / 10")

                st.write("### 📝 Summary")
                st.write(review.summary)

                col3, col4 = st.columns(2)
                with col3:
                    st.write("### ✅ Pros")
                    for pro in review.pros:
                        st.success(f"👍 {pro}")

                with col4:
                    st.write("### ❌ Cons")
                    for con in review.cons:
                        st.warning(f"👎 {con}")

            except Exception as e:
                # All 3 retries failed
                st.error(f"❌ Failed to get a valid response after 3 attempts.\n\nError: {e}")
