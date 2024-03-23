from abc import ABC, abstractmethod
import pygame


class BaseTile(pygame.sprite.Sprite, ABC):
    def __init__(self):
        super().__init__()
        self.image = None
        self.rect = None

    @abstractmethod
    def set_position(self, position) -> None:
        """
        Set the initial position of the tile.
        """
        pass

    @abstractmethod
    def add_placeable_object(self, placeable_object) -> None:
        """
        Add a placeable object to the tile.
        """
        pass

    @abstractmethod
    def remove_placeable_object(self) -> None:
        """
        Remove the placeable object from the tile.
        """
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        """
        Returns whether the tile is empty or not.
        """
        pass
