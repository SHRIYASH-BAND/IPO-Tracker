import asyncio
import json
import os
from zoneinfo import ZoneInfo
from datetime import date, datetime
from typing import Any

from dotenv import load_dotenv
import logging

import httpx
from pydantic import ValidationError
from settings import Settings
from src.abstractClasses.IPOFetcher import IPOFetcher
from src.abstractClasses.IPONotifier import IPONotifier
from src.apiProviders.IpoAlerts import IpoAlerts
from src.service.TelegramNotifier import TelegramIPONotifier

# Configure basic logging
logging.basicConfig(level=logging.INFO)



load_dotenv()

IST = ZoneInfo("Asia/Kolkata")



def build_message(data: dict[str, Any]) -> str:
    """Build a Telegram-friendly summary from the IPOAlerts API response."""

    now = datetime.now(IST)
    today = now.date()

    meta = data.get("meta", {})
    ipos = data.get("ipos", [])

    # Detect an invalid/missing API key response.
    api_info = str(meta.get("info", ""))
    if "valid api key" in api_info.lower():
        raise RuntimeError(
            "IPOAlerts API key is missing or invalid; response may be incomplete."
        )

    if not ipos:
        return (
            f"📈 IPO Watch — {now:%d %b %Y, %I:%M %p IST}\n\n"
            "No IPOs are currently open for subscription."
        )

    lines = [
        f"📈 IPO Watch — {now:%d %b %Y, %I:%M %p IST}",
        f"🟢 {len(ipos)} IPO(s) currently open",
        "",
    ]

    # Cap the output to avoid Telegram's 4,096-character limit.
    for ipo in ipos[:5]:
        name = ipo.get("name", "Unknown company")
        symbol = ipo.get("symbol", "—")
        ipo_type = ipo.get("type", "—")
        source = str(ipo.get("source", "")).upper()

        start_date = ipo.get("startDate", "—")
        end_date = ipo.get("endDate", "—")
        listing_date = ipo.get("listingDate", "—")

        price_range = ipo.get("priceRange", "—")
        lot_size = ipo.get("minQty")
        min_amount = ipo.get("minAmount")
        issue_size = ipo.get("issueSize", "—")

        info_url = ipo.get("infoUrl")
        prospectus_url = ipo.get("prospectusUrl")

        # Determine alert urgency from the IPO closing date.
        urgency = "🟢 Currently open"

        try:
            close_date = date.fromisoformat(end_date)
            days_remaining = (close_date - today).days

            if days_remaining == 0:
                urgency = "🔴 Last day to apply"
            elif days_remaining == 1:
                urgency = "🟠 Closes tomorrow"
            elif days_remaining > 1:
                urgency = f"🟢 Closes in {days_remaining} days"
        except (TypeError, ValueError):
            pass

        lot_size_text = (
            f"{lot_size:,} shares"
            if isinstance(lot_size, int)
            else "—"
        )

        min_amount_text = (
            f"₹{int(min_amount):,}"
            if isinstance(min_amount, (int, float))
            else "—"
        )

        exchange_text = f" • {source}" if source else ""

        lines.extend([
            urgency,
            f"🏢 {name} ({symbol})",
            f"📌 {ipo_type}{exchange_text}",
            f"💰 Price band: ₹{price_range} | Lot: {lot_size_text}",
            f"💳 Minimum investment: {min_amount_text}",
            f"📅 Apply: {start_date} → {end_date}",
            f"📈 Listing: {listing_date} | Issue size: ₹{issue_size}",
        ])

        if info_url:
            lines.append(f"ℹ️ Details: {info_url}")

        if prospectus_url:
            lines.append(f"📄 RHP: {prospectus_url}")

        lines.append("")

    if len(ipos) > 5:
        lines.append(f"…and {len(ipos) - 5} more currently open IPO(s).")
        lines.append("")

    lines.append("⚠️ Information only; not investment advice.")

    return "\n".join(lines)


async def main() -> None:

    # 1. Load & Validate Configuration (Fails early if .env is missing key parameters)
    try:
        config = Settings()
    except ValidationError as e:
        logging.error(f"Configuration error: {e}")
        return


    async with httpx.AsyncClient() as client:

        # 2. Fetch IPO list and build message
        try:
            alerts_provider : IPOFetcher = IpoAlerts()
            data = await alerts_provider.fetchOpenIposList(client, config)
            message = build_message(data)
        except Exception as error:

            logging.error(
                "⚠️ IPO notifier could not retrieve data today.\n"
                f"Error: {type(error).__name__}"
            )
            return

        # 3. Notify the subscribers via notifier bots
        notifier : IPONotifier = TelegramIPONotifier()

        await notifier.notify(client,config,message)


if __name__ == "__main__":
    asyncio.run(main())