
import asyncio

from src.abstractClasses.IPONotifier import IPONotifier
from src.service.DiscordNotifier import DiscordIPONotifier
from src.service.TelegramNotifier import TelegramIPONotifier


class NotifierService:
    """Service to send notifications to various platforms (e.g. Telegram, Discord, Email, etc.)"""

    def __init__(self):
        self.notifierServices : list[IPONotifier] = [
            TelegramIPONotifier(),
            DiscordIPONotifier("https://discord.com/api/webhooks/your_webhook_id/your_webhook_token")
        ]

    async def send_notification(self, client, config, message: str) -> bool:
        """Send a notification using the provided notifiers."""

        tasks = [notifier.notify(client, config, message) for notifier in self.notifierServices]
        
        return any(await asyncio.gather(*tasks))