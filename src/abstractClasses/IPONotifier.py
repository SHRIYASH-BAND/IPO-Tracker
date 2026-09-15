import httpx


from abc import ABC, abstractmethod

from settings import Settings


class IPONotifier(ABC):
    """
    Abstract Base Class defining the interface for IPO notification dispatchers.
    """

    @abstractmethod
    async def notify(self, 
        client: httpx.AsyncClient,
        config : Settings,
        message: str) -> bool:
        """
        Sends an IPO alert message.

        Must be overridden by all subclasses.
        """
        pass

    @abstractmethod
    async def authenticate(self) -> None:
        """
        Handles credentials and connection setup.
        """
        pass