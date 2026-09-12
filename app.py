import asyncio
import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv

import httpx


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


async def send_telegram(client: httpx.AsyncClient, message: str) -> None:
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_ids = os.environ["TELEGRAM_CHAT_IDS"].split(",")

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    for chat_id in chat_ids:
        response = await client.post(
            url,
            json={
                "chat_id": chat_id.strip(),
                "text": message,
                "disable_web_page_preview": True,
            },
            timeout=30,
        )
        response.raise_for_status()


async def send_discord(client: httpx.AsyncClient, message: str) -> None:
    webhook_url = os.environ["DISCORD_WEBHOOK_URL"]

    response = await client.post(
        webhook_url,
        json={"content": message},
        timeout=30,
    )
    response.raise_for_status()


async def main() -> None:
    send_to = os.environ.get("SEND_TO", "telegram").lower()

    async with httpx.AsyncClient() as client:
        try:
            data = await fetch_data(client)
            message = build_message(data)
        except Exception as error:
            message = (
                "⚠️ IPO notifier could not retrieve data today.\n"
                f"Error: {type(error).__name__}"
            )

        if send_to in {"telegram", "both"}:
            await send_telegram(client, message)

        if send_to in {"discord", "both"}:
            await send_discord(client, message)


if __name__ == "__main__":
    asyncio.run(main())