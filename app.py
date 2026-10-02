import asyncio
import json
import os


from typing import Any

from dotenv import load_dotenv
import logging

import httpx
from pydantic import ValidationError
from src.apiProviders.UpstoxApi import UpstoxApi
from src.service.UniformMessageBuilder import UniformMessageBuilder
from src.service.NotifierService import NotifierService
from settings import Settings
from src.abstractClasses.IPOFetcher import IPOFetcher
from src.abstractClasses.IPONotifier import IPONotifier
from src.apiProviders.IpoAlerts import IpoAlerts
from src.service.TelegramNotifier import TelegramIPONotifier

# Configure basic logging
logging.basicConfig(level=logging.INFO)



load_dotenv()

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
            message_builder : UniformMessageBuilder = UniformMessageBuilder()

            #alerts_provider : IPOFetcher = IpoAlerts()
            alerts_provider : IPOFetcher = UpstoxApi()

            data = await alerts_provider.fetchOpenIposList(client, config)
            
            #message = message_builder.build_message_ipoalerts(data)
            message = message_builder.build_message_upstox(data)
        except Exception as error:

            logging.error(
                "⚠️ IPO notifier could not retrieve data today.\n"
                f"Error: {type(error).__name__}"
            )
            return

        # 3. Notify the subscribers via notifier bots
        notifierService : NotifierService = NotifierService()

        await notifierService.send_notification(client, config, message)


if __name__ == "__main__":
    asyncio.run(main())