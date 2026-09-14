import logging
import httpx

from settings import Settings
from src.abstractClasses.IPONotifier import IPONotifier


class TelegramIPONotifier(IPONotifier):
    """
        Telegram Notifier Bot for IPO notifications through chat ids.
    """

    SEND_MSG_URL :str

    def __init__(self, bot_token: str, chat_ids: list[str]):
        self.bot_token = bot_token
        self.chat_ids = chat_ids
        self.SEND_MSG_URL = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        

    async def authenticate(self) -> None:
        logging.info("Authenticating Telegram Bot API token...")

    async def notify(self, client: httpx.AsyncClient, message: str) -> bool:
        logging.info(f"[Telegram -> Chat {self.chat_id}]: {message}")

        try:
            for chat_id in self.chat_ids:
                response = await client.post(
                    self.SEND_MSG_URL,
                    json={
                        "chat_id": chat_id.strip(),
                        "text": message,
                        "disable_web_page_preview": True,
                    },
                    timeout=30,
                )
                response.raise_for_status()

        except Exception as error:
            logging.error(f"Error Occurred in telegram notification : ${error}")
            return False

        return True
