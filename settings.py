from pydantic import HttpUrl, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Loads and validates configuration from environment variables or .env file."""

    api_url: HttpUrl
    api_key: SecretStr
    telegram_bot_token: SecretStr
    telegram_chat_id: str
    discord_webhook_url: HttpUrl
    excel_file_path: str = "ipo_tracker.xlsx"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )