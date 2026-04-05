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
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # 1. Define a generator to consume the FastAPI stream
        def get_backend_stream():
            try:
                response = requests.post(
                    settings.FASTAPI_ENDPOINT,
                    json={"message": prompt},
                    stream=True  
                )
                for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                    if chunk:
                        yield chunk
            except requests.exceptions.RequestException as e:
                st.error(f"⚠️ Connection error: {e}")
                yield f"Oops! I had trouble connecting to my brain. Error: {str(e)}"

        # 2. Use Streamlit's native streaming UI component
        full_response = st.write_stream(get_backend_stream())
        
        # 3. Save the final string to session state
        st.session_state.messages.append({"role": "assistant", "content": full_response})