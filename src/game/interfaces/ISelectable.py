from abc import ABC, abstractmethod

from src.game.interfaces.IHoverable import IHoverable

class ISelectable(IHoverable, ABC):
    pass