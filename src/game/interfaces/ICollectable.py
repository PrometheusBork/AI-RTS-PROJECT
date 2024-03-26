from abc import ABC, abstractmethod

from game.interfaces.IAttackable import IAttackable


class ICollectable(IAttackable, ABC):
    @abstractmethod
    def get_resource(self) -> None:
        """
        Collect resource from collectable object.
        """
        pass
