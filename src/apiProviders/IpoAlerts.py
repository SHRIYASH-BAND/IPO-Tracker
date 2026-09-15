import json
import httpx
from typing import Any, Dict, List, Optional

from settings import Settings
from src.abstractClasses.IPOFetcher import IPOFetcher
from src.modal import IPORecord


class IpoAlerts(IPOFetcher):

    """
    IPO Alerts URL
    """

    
    async def get_ipos(self,
            client: httpx.AsyncClient,
            config: Settings,
            status: Optional[str] = None, 
            type: Optional[str] = None,
            page: int = 1,
            limit: int = 1) -> Dict:

        """Get IPOs with optional filtering and pagination."""

        params = {
            "page": page,
            "limit": limit
        }

        # open/closed... 
        if status:
            params |= {"status": status}

        # sme / mainboard ...
        if type:
            params |= {"type": type}

        response = await client.get(
            str(config.ipo_alerts_api_url),
            params=params,
            headers={
                "Accept": "application/json",
                "x-api-key": config.ipo_alerts_api_key.get_secret_value(),
            },
            timeout=30,
        )
        
        response.raise_for_status()
        return response.json()

    async def fetchOpenIposList(self, client: httpx.AsyncClient, config: Settings) -> Any:
        """
        Fetches the IPOs opened list.

        Must be overridden by all subclasses.
        """
        return await self.get_ipos(client, config, "open")


    async def transformToIPOModel(self, response: str) -> Any:
        """
        Converts Response of API to local standard modal.
        """
        pass