from typing import Any

from pydantic import HttpUrl, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Loads and validates configuration from environment variables or .env file."""

    ipo_alerts_api_url: HttpUrl
    ipo_alerts_api_key: SecretStr
    telegram_bot_token: SecretStr
    telegram_chat_ids: str
    #discord_webhook_url: HttpUrl
    #excel_file_path: str = "ipo_tracker.xlsx"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )

    def __init__(self, **values: Any) -> None:
        super().__init__(**values)