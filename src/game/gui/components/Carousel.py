import pygame_gui

class Carousel(pygame_gui.elements.UIPanel):
    def __init__(self, relative_rect, manager, container, object_id):
        super().__init__(
            relative_rect=relative_rect, 
            manager=manager, 
            container=container, 
            object_id=object_id
            )
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def scroll(self, direction):
        # Assuming horizontal scrolling, adjust the x position of each item
        for item in self.items:
            item.rect.x += direction * 10  # Adjust the scrolling speed as needed
            if item.rect.right < 0:
                item.rect.x = self.rect.width
            elif item.rect.left > self.rect.width:
                item.rect.x = -item.rect.width
