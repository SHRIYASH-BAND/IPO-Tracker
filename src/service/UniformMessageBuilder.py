from datetime import date, datetime
from zoneinfo import ZoneInfo

from typing import Any


IST = ZoneInfo("Asia/Kolkata")

class UniformMessageBuilder:
    """
    A class to build uniform messages for IPO records.
    """

    @staticmethod
    def build_message_ipoalerts(data: dict[str, Any]) -> str:
        """Build a Telegram-friendly summary from the IPOAlerts API response."""

        now = datetime.now(IST)
        today = now.date()

        meta = data.get("meta", {})
        ipos = data.get("ipos", [])

      
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

    @staticmethod
    def build_message_upstox(data: dict[str, Any]) -> str:
        """Build a Telegram-friendly summary from the Upstox API response."""

        now = datetime.now(IST)
        today = now.date()

        ipos = data.get("data", [])

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
            industry = ipo.get("industry", "—")
            ipo_type = ipo.get("issue_type", "—")
           
            start_date = ipo.get("bidding_start_date", "—")
            end_date = ipo.get("bidding_end_date", "—")
            

            min_amount = ipo.get("minimum_price")
            max_amount = ipo.get("maximum_price")
            issue_size = ipo.get("issue_size", "—")
            
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

            
            issue_size_text = (
                f"{issue_size:,} Cr"
                if isinstance(issue_size, float)
                else "—"
            )
           
            min_amount_text = (
                f"₹{int(min_amount):,}"
                if isinstance(min_amount, (int, float))
                else "—"
            )

            lines.extend([
                urgency,
                f"🏢 {name} ({symbol})",
                f"📌 Issue Type: {ipo_type}",
                f"💰 Issue Size: ₹{issue_size_text}",
                f"💰 Price band: ₹{min_amount} | ₹{max_amount} ",
                f"💳 Minimum investment: {min_amount_text}",
                f"📅 Apply: {start_date} → {end_date}",
            ])
    
            lines.append("")

        if len(ipos) > 5:
            lines.append(f"…and {len(ipos) - 5} more currently open IPO(s).")
            lines.append("")

        lines.append("⚠️ Information only; not investment advice.")

        return "\n".join(lines)