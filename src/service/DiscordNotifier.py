import logging
import httpx

from settings import Settings
from src.abstractClasses.IPONotifier import IPONotifier


class DiscordIPONotifier(IPONotifier):

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    async def authenticate(self) -> None:
        logging.info("Validating Discord Webhook URL...")

    async def notify(self, client: httpx.AsyncClient, config : Settings, message: str) -> bool:
        logging.info(f"[Discord Webhook]: {message}")
        # Add requests.post(self.webhook_url, json={"content": message}) here
        # webhook_url = os.environ["DISCORD_WEBHOOK_URL"]
        
        #     response = await client.post(
        #         webhook_url,
        #         json={"content": message},
        #         timeout=30,
        #     )
        #     response.raise_for_status()
        return True