from functools import lru_cache
from typing import Literal
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_url: str = "http://localhost:11434"
    model_api_key: str = ""
    model_name: str = "qwen3:4b"
    model_provider: Literal["openai", "anthropic", "local"] = "local"
    database_url: str = ""
    hf_token: str = ""

    image_height: int = 400
    image_width: int = 400


@lru_cache(maxsize=None)
def get_settings():
    return Settings()
