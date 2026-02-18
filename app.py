import streamlit as st
from groq import Groq
import os

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are a helpful coding assistant.
You generate clean, well‑structured code in Python, Java, JavaScript, or other languages based on user requirements.
Always explain your code briefly and provide best practices.
Provide efficient single Code with respect to Exam situation.
Provide the answer to next question with relate current response.
Example situation :If someone asks u to write a code to write a calculator application code and later if he asks to create a user interface for that try to build entire ui based application and provide Url for that.
If requirements are unclear, ask clarifying questions before writing code.
"""

# Function to set background with reduced brightness
def set_bg(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)),
                        url("{image_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Function to reset background to blank
def reset_bg():
    st.markdown(
        """
        <style>
        .stApp {
            background: none !important;
            background-color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Show wallpaper only before user asks a question
if "asked" not in st.session_state:
    set_bg("https://static.vecteezy.com/system/resources/previews/024/150/449/non_2x/artificial-intelligence-robot-on-computer-screen-vector.jpg")
else:
    reset_bg()

# Chatbot UI
st.title("(｡◕‿◕｡) Code Writing Chatbot")
st.caption("Powered by GROQ AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Describe the code you need..."):
    st.session_state.asked = True  # switch background off after first question

    # Save and display user message immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Build conversation
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

    # Save and display assistant reply
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
