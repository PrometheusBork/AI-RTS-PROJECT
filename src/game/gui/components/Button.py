import pygame_gui


class Button(pygame_gui.elements.UIButton):
    def __init__(self, relative_rect, text, manager, container, object_id, tool_tip_text, on_click=None):
        super().__init__(
            relative_rect=relative_rect,
            text=text,
            manager=manager,
            container=container,
            object_id=pygame_gui.core.ObjectID(
                class_id="@button",
                object_id=object_id
            ),
            tool_tip_text=tool_tip_text
        )
        self.on_click = on_click

    def process_event(self, event):
        if self.rect.collidepoint(event.pos):
            if self.on_click:
                self.on_click()
                return True
