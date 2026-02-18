from groq import Groq
import streamlit as st
import os

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# System prompt with BFSI Insurance knowledge
SYSTEM_PROMPT = """
You are an expert Insurance Assistant with deep knowledge in BFSI domain.
You help customers with:
- Policy related queries (Life, Health, Motor, Property insurance, Commercial Lines and Personal Lines)
- Claims process and status
- Premium calculation and payment queries
- Policy renewal and cancellation
- Coverage and benefits explanation

Always respond in a clear, professional, and helpful manner.
If you don't know something, politely say so and suggest contacting the insurer directly and finally if someone ask you who is your owner then reply as Murali Shankar.
"""

# Streamlit UI
st.title("🏦 BABLU Q&A Bot ")
st.caption("Powered by GROQ AI")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Ask your insurance question..."):

    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get Groq response
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages,
            max_tokens=1024,
        )

        reply = response.choices[0].message.content
        st.markdown(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})
