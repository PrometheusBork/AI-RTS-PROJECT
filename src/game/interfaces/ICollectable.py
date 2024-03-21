from abc import ABC, abstractmethod


class ICollectable(ABC):
    @abstractmethod
    def collect(self) -> None:
        """
        Collect resource from collectable object.
        """
        pass