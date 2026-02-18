from groq import Groq
import streamlit as st
import os

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are a helpful coding assistant.
You generate clean, well‑structured code in Python, Java, JavaScript, or other languages based on user requirements.
Always explain your code briefly and provide best practices.
Provide efficient single Code with respect to Exam situation.
If requirements are unclear, ask clarifying questions before writing code.
"""

st.title("(｡◕‿◕｡) BABLU")
st.caption("Powered by GROQ AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Describe the code you need..."):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=1024,
    )
    reply = response.choices[0].message.content
    st.markdown(reply)

    # Save history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": reply})
