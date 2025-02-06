import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


st.title("Liiaa")

client = OpenAI(
    base_url="https://api.deepseek.com", api_key=os.getenv("DEEPSEEK_API_KEY")
)


if "message" not in st.session_state:
    st.session_state["message"] = []

if "model" not in st.session_state:
    st.session_state["model"] = "deepseek-chat"

for msg in st.session_state["message"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input():
    st.session_state["message"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="deepseek-reasoner",
            messages=st.session_state["message"],
            stream=True,
        )
        response = st.write_stream(stream)

    st.session_state["message"].append({"role": "assistant", "content": response})
