from abc import ABC, abstractmethod
import pygame


class BaseGameObject(pygame.sprite.Sprite, ABC):
    def __init__(self):
        super().__init__()
        self.image = None
        self.rect = None

    @abstractmethod
    def set_position(self, position) -> None:
        """
        Set the initial position of the game object.
        """
        pass
