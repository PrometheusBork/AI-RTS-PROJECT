from abc import ABC, abstractmethod


class IHoverable(ABC):
    @abstractmethod
    def render_hover(self, screen):
        pass

    @abstractmethod
    def is_hovered(self, mouse_pos):
        pass
