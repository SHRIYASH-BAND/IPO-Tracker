import json
import httpx
from typing import Any, Dict, List, Optional

from pydantic import config

from settings import Settings
from src.abstractClasses.IPOFetcher import IPOFetcher
from src.modal import IPORecord

class UpstoxApi(IPOFetcher):

    """
    Upstox api for IPOs
    """

    
    async def get_ipos(self,
            client: httpx.AsyncClient,
            config: Settings,
            issue_type: str) -> Dict:

        """Get IPOs"""

        params = {
            "status": "open",
            "issue_type": issue_type,
            "page_number": 1,
            "records":30
        }

        response = await client.get(
            str(config.upstox_api_url),
            params=params,
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {config.upstox_analytics_api_key.get_secret_value()}",
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

        #fetch issue_type = "sme"
        sme_ipos = await self.get_ipos(client, config, "sme")
        
        #fetch issue_type = "regular"
        regular_ipos = await self.get_ipos(client, config, "regular")

        # Combine the results from both calls
        combined_ipos = regular_ipos.get("data", []) + sme_ipos.get("data", [])

        return {"data": combined_ipos}


    async def transformToIPOModel(self, response: str) -> Any:
        """
        Converts Response of API to local standard modal.
        """
        pass