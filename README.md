# llm-chatbot

folder structure
llm-chatbot/
├── .env                # API Keys (OPENAI_API_KEY, etc.)
├── .gitignore          # Ignore __pycache__, .env, and venv
├── requirements.txt    # langchain, langgraph, fastapi, uvicorn, pydantic-settings
├── app/
│   ├── __init__.py
│   ├── main.py         # Entry point: FastAPI app initialization
│   ├── core/           # System-wide configuration
│   │   ├── __init__.py
│   │   └── config.py   # Settings management via Pydantic
│   ├── api/            # API Layer
│   │   ├── __init__.py
│   │   ├── routes.py   # Chat endpoints
│   │   └── schemas.py  # Pydantic models (Request/Response)
│   └── services/       # Logic Layer (The Graph)
│       ├── __init__.py
│       ├── graph.py    # Graph compilation and workflow
│       ├── nodes.py    # Node functions (LLM logic)
│       └── state.py    # LangGraph State definitions
└── tests/              # (Future) Unit and integration tests