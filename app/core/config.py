from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

class Settings(BaseSettings):
    # Provider Selection: 'ollama' | 'openai' | 'openrouter'
    LLM_PROVIDER: Literal["ollama", "openai", "openrouter"] = "ollama"
    
    # Ollama Settings
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "gemma4:e2b"

    # OpenAI / OpenRouter Settings
    OPENAI_API_KEY: str | None = None
    OPENROUTER_API_KEY: str | None = None
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()