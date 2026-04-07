import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
import requests
from app.core.config import settings
import uuid

st.set_page_config(page_title="Staff AI Research Agent", page_icon="🤖")

st.title("🤖 AI Research Assistant")
st.caption("Backend: FastAPI + LangGraph | LLM: Ollama/OpenRouter")

# 1. Sidebar for Session Management
with st.sidebar:
    st.header("Session Settings")
    st.markdown("---")
    
    # Persistent Conversation ID (Thread ID)
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(uuid.uuid4())
    
    thread_id = st.text_input(
        "Conversation ID", 
        value=st.session_state.thread_id,
        help="Paste a previous Conversation ID to resume that session."
    )
    
    # Update state if changed
    if thread_id != st.session_state.thread_id:
        st.session_state.thread_id = thread_id
        # Optional: Clear messages from view when switching sessions (they'll be re-loaded from server if needed)
        st.session_state.messages = []
        st.rerun()

    st.info(f"Active Session: `{st.session_state.thread_id}`")
    
    if st.button("New Session"):
        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()

# 2. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Display existing messages from session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Chat Input
if prompt := st.chat_input("What's on your mind?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Define a generator to consume the FastAPI stream
        def get_backend_stream():
            try:
                response = requests.post(
                    settings.FASTAPI_ENDPOINT,
                    json={
                        "message": prompt,
                        "thread_id": st.session_state.thread_id
                    },
                    stream=True  
                )
                for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                    if chunk:
                        yield chunk
            except requests.exceptions.RequestException as e:
                st.error(f"⚠️ Connection error: {e}")
                yield f"Oops! I had trouble connecting to my brain. Error: {str(e)}"

        # Use Streamlit's native streaming UI component
        full_response = st.write_stream(get_backend_stream())
        
        # Save the final string to session state
        st.session_state.messages.append({"role": "assistant", "content": full_response})