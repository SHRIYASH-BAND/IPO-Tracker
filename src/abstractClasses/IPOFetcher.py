from typing import Any

import httpx


from abc import ABC, abstractmethod

from settings import Settings
from src.modal import IPORecord


class IPOFetcher(ABC):
    """
    Abstract Base Class defining the interface for IPO fetching services.
    """

    @abstractmethod
    async def fetchOpenIposList(self, client: httpx.AsyncClient, config: Settings) -> Any:
        """
        Fetches the IPOs opened list.

        Must be overridden by all subclasses.
        """
        return None

    @abstractmethod
    async def transformToIPOModel(self, response: str) -> Any:
        """
        Converts Response of API to local standard modal.
        """
        return None