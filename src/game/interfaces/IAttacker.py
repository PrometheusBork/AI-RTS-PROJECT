from abc import ABC, abstractmethod


class IAttacker(ABC):
    @property
    @abstractmethod
    def damage(self) -> int:
        """
        Get the damage of the attacker object.
        """
        pass

    @abstractmethod
    def attack(self, attackable_object) -> None:
        """
        Object attacks an attackable object.
        """
        pass
