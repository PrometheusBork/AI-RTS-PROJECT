from abc import ABC, abstractmethod

class ICollect(ABC):
    @abstractmethod
    def collect(self) -> None:
        """
        Collect resource from collectable object.
        """
        pass