from abc import ABC, abstractmethod


class IMovable(ABC):
    @abstractmethod
    def get_position(self) -> tuple[int, int]:
        """
        Returns the current position of the movable object.
        """
        pass

    @abstractmethod
    def update_position(self, new_position) -> None:
        """
        Updates the position of the movable object to the given new position.
        """
        pass
