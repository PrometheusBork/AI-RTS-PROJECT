from abc import ABC, abstractmethod


class ICollector(ABC):
    @abstractmethod
    def collect(self, collectable_object) -> None:
        """
        Object collects a collectable object.
        """
        pass
