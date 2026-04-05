from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from app.core.config import settings

def get_model():
    if settings.LLM_PROVIDER == "ollama":
        return ChatOllama(
            base_url=settings.OLLAMA_BASE_URL,
            model=settings.OLLAMA_MODEL
        )
    elif settings.LLM_PROVIDER == "openai":
        return ChatOpenAI(api_key=settings.OPENAI_API_KEY, model="gpt-4o")
    elif settings.LLM_PROVIDER == "openrouter":
        return ChatOpenAI(
            api_key=settings.OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
            model="anthropic/claude-3.5-sonnet"
        )
    raise ValueError(f"Unsupported provider: {settings.LLM_PROVIDER}")