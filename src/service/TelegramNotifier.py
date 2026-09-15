import logging
import httpx

from settings import Settings
from src.abstractClasses.IPONotifier import IPONotifier


class TelegramIPONotifier(IPONotifier):
    """
        Telegram Notifier Bot for IPO notifications through chat ids.
    """


    async def authenticate(self) -> None:
        logging.info("Authenticating Telegram Bot API token...")

    async def notify(self, client: httpx.AsyncClient, config : Settings, message: str) -> bool:

        chat_ids = config.telegram_chat_ids.split(",")
        send_msg_url = f"https://api.telegram.org/bot{config.telegram_bot_token.get_secret_value()}/sendMessage"

        logging.info(f"[Telegram -> Chat {config.telegram_chat_ids}]: {message}")


        try:
            for chat_id in chat_ids:
                response = await client.post(
                    send_msg_url,
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
