from game.interfaces.IObserver import IObserver
from game.interfaces.IHoverable import IHoverable
from game.interfaces.IObserveable import IObserveable


class HoverRenderer(IObserver):
    def __init__(self, game_world):
        self.hoverable_objects = []
        self.game_world = game_world
        self.register_hoverable_objects()

    def register_hoverable_objects(self):
        for row in self.game_world.map:
            for tile in row:
                self.add_hoverable_object(tile)
                if not tile.is_empty():
                    self.add_hoverable_object(tile.game_object)

        # Sort the hoverable objects by their hover priority
        self.sort_hoverable_objects()

    def add_hoverable_object(self, hoverable_object):
        if isinstance(hoverable_object, IHoverable):
            self.hoverable_objects.append(hoverable_object)
            if isinstance(hoverable_object, IObserveable):
                hoverable_object.register(self)
        return self

    def remove_hoverable_object(self, hoverable_object):
        if hoverable_object in self.hoverable_objects:
            self.hoverable_objects.remove(hoverable_object)

    def render_hover(self, mouse_pos, screen):
        hovered_object = next((hoverable_object for hoverable_object in self.hoverable_objects if hoverable_object.is_hovered(mouse_pos)), None)
        if hovered_object:
            hovered_object.render_hover(screen)

    def sort_hoverable_objects(self):
        self.hoverable_objects.sort(key=lambda obj: obj.get_hover_priority())

    def update(self, hoverable_object):
        self.remove_hoverable_object(hoverable_object)

    def reset(self, game_world):
        self.hoverable_objects = []
        self.game_world = game_world
        self.register_hoverable_objects()
