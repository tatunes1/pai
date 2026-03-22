from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    es_host: str = "http://localhost:9200"
    es_index: str = "rag_documents"
    es_vector_dims: int = 384

    embed_model: str = "all-MiniLM-L6-v2"

    #LLM
    llm_provider: str = "None"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o"
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-4-20250514"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3"

    #RAG
    top_k: int = 5
    chunk_size: int = 500
    chunk_overlap:int = 50

    class Config:
        env_file = ".env"
        extra = "ignore"

@lru_cache
def get_settings() -> Settings:
    return Settings()