from abc import ABC, abstractmethod

from game.interfaces.IObserveable import IObserveable


class IAttackable(IObserveable, ABC):
    @property
    @abstractmethod
    def health(self) -> int:
        """
        Get the current health of the attackable object.
        """
        pass

    @abstractmethod
    def take_damage(self, damage) -> None:
        """
        Apply damage to the attackable object.
        """
        pass

    @abstractmethod
    def is_destroyed(self) -> bool:
        """
        Check if the attackable object is destroyed (health <= 0).
        """
        pass
