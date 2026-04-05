# 🤖 Staff AI Research Agent

A full-stack, streaming-enabled AI Chatbot built with **FastAPI**, **LangGraph**, and **Streamlit**. Supporting both local (Ollama) and cloud (OpenAI/OpenRouter) LLM providers.

## 🚀 Features

- **Streaming Architecture**: Real-time token streaming from LangGraph to Streamlit.
- **Stateful Logic**: Powered by LangGraph for robust agentic workflows.
- **Provider Flexibility**: Seamlessly switch between Ollama, OpenAI, and OpenRouter.
- **Dockerized**: Production-ready containerization with Docker Compose.
- **Safe Networking**: Configured for internal service communication within Docker.

## 📂 Project Structure

```text
llm-chatbot/
├── app/
│   ├── api/            # FastAPI routes and streaming logic
│   ├── core/           # Configuration and Pydantic settings
│   ├── services/       # LangGraph integration, nodes, and LLM setup
│   ├── ui/             # Streamlit chat interface
│   └── main.py         # Backend entry point
├── Dockerfile.api      # FastAPI Docker specification
├── Dockerfile.ui       # Streamlit Docker specification
├── docker-compose.yml  # Multi-container orchestration
└── requirements.txt    # Project dependencies
```

## 🛠️ Setup & Installation

### 1. Prerequisites
- Python 3.11+
- Docker (optional, for containerized run)
- [Ollama](https://ollama.ai/) (optional, for local LLMs)

### 2. Configure Environment
Create a `.env` file in the root directory:
```bash
LLM_PROVIDER=ollama  # ollama | openai | openrouter
OLLAMA_MODEL=gemma2:2b
OPENAI_API_KEY=your_key_here
```

### 3. Run with Docker (Recommended)
The easiest way to run the full stack:
```bash
docker compose up --build
```
- **UI**: [http://localhost:8501](http://localhost:8501)
- **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

### 4. Run Locally (Development)
If you prefer running without Docker:

**Backend (FastAPI):**
```bash
export PYTHONPATH=$PYTHONPATH:.
python app/main.py
```

**Frontend (Streamlit):**
```bash
streamlit run app/ui/chat_interface.py
```

## 🔌 API Endpoints

- `POST /v1/chat`: Standard synchronous completion.
- `POST /v1/chat/stream`: Real-time streaming completion (used by the UI).
