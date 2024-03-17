from abc import ABC, abstractmethod
import pygame


class IRenderable(ABC):
    @abstractmethod
    def get_sprite_group(self) -> pygame.sprite.Group:
        """
        Returns the sprite group associated with this renderable object.
        """
        pass

    @abstractmethod
    def has_debug_info(self) -> bool:
        """
        Returns True if the renderable object has debug information to be rendered, False otherwise.
        """
        pass

    @abstractmethod
    def get_debug_info(self) -> str:
        """
        Returns the debug information string for the given sprite.
        """
        pass

    @abstractmethod
    def get_render_priority(self) -> int:
        """
        Returns the priority of the renderable object.
        Lower values have higher priority.
        """
        pass
