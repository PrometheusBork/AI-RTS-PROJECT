from abc import ABC, abstractmethod


class IHoverable(ABC):
    @abstractmethod
    def is_hovered(self, mouse_pos) -> bool:
        """
        Returns True if the object is hovered by the mouse cursor at the given position, False otherwise.
        """
        pass

    @abstractmethod
    def render_hover(self, surface) -> None:
        """
        Renders the hover effect for this object on the given surface.
        """
        pass

    @abstractmethod
    def get_hover_priority(self) -> int:
        """
        Returns the priority value for rendering the hover effect.
        Lower values have higher priority.
        """
        pass