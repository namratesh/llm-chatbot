import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
import requests
from app.core.config import settings
st.set_page_config(page_title="Staff AI Research Agent", page_icon="🤖")

st.title("🤖 AI Research Assistant")
st.caption("Backend: FastAPI + LangGraph | LLM: Ollama/OpenRouter")

# 1. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Display existing messages from session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Chat Input
if prompt := st.chat_input("What's on your mind?"):
    # Add user message to UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 4. Call FastAPI Backend
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    settings.FASTAPI_ENDPOINT,
                    json={"message": prompt},
                    timeout=60
                )
                if response.status_code == 200:
                    ai_response = response.json().get("response")
                    st.markdown(ai_response)
                    # Save AI response
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                else:
                    st.error(f"Error: {response.status_code}")
            except Exception as e:
                st.error(f"Connection failed: {e}")