import pygame_gui


class Button(pygame_gui.elements.UIButton):
    def __init__(self, rect, text, manager, container, on_click=None):
        super().__init__(
            relative_rect=rect,
            text=text,
            manager=manager,
            container=container,
            object_id=pygame_gui.core.ObjectID(
                class_id="@button",
                object_id="#button"
            )
        )
        self.on_click = on_click

    def handle_events(self, events):
        pass
