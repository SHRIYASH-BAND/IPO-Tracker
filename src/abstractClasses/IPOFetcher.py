import httpx


from abc import ABC, abstractmethod

from src.modal import IPORecord


class IPOFetcher(ABC):
    """
    Abstract Base Class defining the interface for IPO fetching services.
    """

    @abstractmethod
    async def fetchOpenIposList(self, client: httpx.AsyncClient) -> any:
        """
        Fetches the IPOs opened list.

        Must be overridden by all subclasses.
        """
        pass

    @abstractmethod
    async def transformToIPOModel(self, response: str) -> IPORecord:
        """
        Converts Response of API to local standard modal.
        """
        pass