import os

from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parents[1] / ".env")


@dataclass(frozen=True)
class Config:
    """Настройки окружения: адреса и токен."""

    api_base_url: str
    web_url: str
    api_key: str


def load_config() -> Config:
    """Читает переменные окружения и возвращает конфигурацию."""
    api_key: str | None = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("Не задан API_KEY: скопируйте .env.example в .env")
    return Config(
        api_base_url=os.getenv("API_BASE_URL", "https://api.kinopoisk.dev"),
        web_url=os.getenv("WEB_URL", "https://www.kinopoisk.ru"),
        api_key=api_key,
    )
