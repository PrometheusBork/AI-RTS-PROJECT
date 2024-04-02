from abc import ABC, abstractmethod

from game.interfaces.IHoverable import IHoverable

class ISelectable(IHoverable, ABC):
    pass