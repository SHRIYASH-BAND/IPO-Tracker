import requests
import json
import httpx
from typing import Dict, List, Optional

from src.abstractClasses.IPOFetcher import IPOFetcher


class IpoAlerts(IPOFetcher):

    """
    IPO Alerts URL
    """

    BASE_URL: str = "https://api.ipoalerts.in"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "x-api-key": api_key,
            "Content-Type": "application/json"
        })
    
    async def get_ipos(self,
            client: httpx.AsyncClient,
            status: Optional[str] = None, 
            type: Optional[str] = None,
            page: int = 1,
            limit: int = 10) -> Dict:

        """Get IPOs with optional filtering and pagination."""

        params = {
            "page": page,
            "limit": limit
        }

        # open/closed... 
        if status:
            params["status"] = status

        # sme / mainboard ...
        if type:
            params["type"] = type

        response = await client.post(
                f"{self.BASE_URL}/ipos",
                params,
                timeout=30,
            )
        
        response.raise_for_status()
        return response.json()

    async def fetchOpenIposList(self, client: httpx.AsyncClient) -> any:
        """
        Fetches the IPOs opened list.

        Must be overridden by all subclasses.
        """
        return self.get_ipos("open")


    async def transformToIPOModel(self, response: str) -> IPORecord:
        """
        Converts Response of API to local standard modal.
        """
        pass