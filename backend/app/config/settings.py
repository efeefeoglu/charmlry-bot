from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    app_name: str = 'Shopify Chatbot MVP'
    google_api_key: str = Field(default='', alias='GOOGLE_API_KEY')
    gemini_model: str = Field(default='gemini-flash-lite-latest', alias='GEMINI_MODEL')
    cors_origins_raw: str = Field(default='*', alias='CORS_ORIGINS')

    @property
    def cors_origins(self) -> List[str]:
        if self.cors_origins_raw.strip() == '*':
            return ['*']
        return [item.strip() for item in self.cors_origins_raw.split(',') if item.strip()]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
