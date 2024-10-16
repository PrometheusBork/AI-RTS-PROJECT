from abc import ABC, abstractmethod

from src.game.interfaces.IAttackable import IAttackable


class ICollectable(IAttackable, ABC):
    @abstractmethod
    def get_resource(self) -> None:
        """
        Collect resource from collectable object.
        """
        pass
