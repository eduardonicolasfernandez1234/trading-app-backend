from abc import ABC, abstractmethod


class BaseSignalParser(ABC):

    @abstractmethod
    def parse(self, message: str) -> dict | None:
        pass
