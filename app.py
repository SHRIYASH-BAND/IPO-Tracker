import asyncio
import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
from pydantic import ValidationError
import logging

import httpx
from settings import Settings
from src.abstractClasses import IPONotifier
from src.service.TelegramNotifier import TelegramIPONotifier

# Configure basic logging
logging.basicConfig(level=logging.INFO)



load_dotenv()

API_URL = os.environ.get("IPO_ALERTS_API_KEY", "https://example.com/api/ipos")
IST = ZoneInfo("Asia/Kolkata")


async def fetch_data(client: httpx.AsyncClient) -> dict:
    """Fetch data from your chosen API."""
    response = await client.get(
        API_URL,
        headers={"Accept": "application/json"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def build_message(data: dict) -> str:
    """
    Convert the API response into a readable notification.

    Adjust this function once you know your API's exact JSON format.
    """
    now = datetime.now(IST).strftime("%d %b %Y, %I:%M %p IST")

    # Example only: assumes API returns {"ipos": [{"company": "...", "close_date": "..."}]}
    ipos = data.get("ipos", [])

    if not ipos:
        return f"📈 IPO Watch — {now}\n\nNo active IPOs were returned today."

    lines = [f"📈 IPO Watch — {now}", ""]
    for ipo in ipos[:10]:
        company = ipo.get("company", "Unknown company")
        close_date = ipo.get("close_date", "date unavailable")
        lines.append(f"• {company} — closes {close_date}")

    return "\n".join(lines)



async def main() -> None:

    # 1. Load & Validate Configuration (Fails early if .env is missing key parameters)
    try:
        config = Settings()
    except ValidationError as e:
        logging.error(f"Configuration error: {e}")
        return False


    async with httpx.AsyncClient() as client:

        # 2. Fetch IPO list and build message
        try:
            data = await fetch_data(client)
            message = build_message(data)
        except Exception as error:

            logging.error(
                "⚠️ IPO notifier could not retrieve data today.\n"
                f"Error: {type(error).__name__}"
            )
            return False

        # 3. Notify the subscribers via notifier bots
        notifier : IPONotifier = TelegramIPONotifier(
            config.telegram_bot_token,
            config.telegram_chat_id
        )

        return notifier.notify(client, message)


if __name__ == "__main__":
    asyncio.run(main())