from game.interfaces.IObserver import IObserver
from game.interfaces.ISelectable import ISelectable
from game.interfaces.IObserveable import IObserveable


class SelectionManager(IObserver):
    def __init__(self, game_world):
        self.game_world = game_world
        self.selectable_objects = set()
        self.selected_object = None
        self.register_selectable_objects()

    def register_selectable_objects(self):
        for row in self.game_world.map:
            for tile in row:
                if not tile.is_empty():
                    self.add_selectable_object(tile.game_object)

    def add_selectable_object(self, selectable_object):
        if isinstance(selectable_object, ISelectable):
            self.selectable_objects.add(selectable_object)
            if isinstance(selectable_object, IObserveable):
                selectable_object.register(self)

    def remove_selectable_object(self, selectable_object):
        self.selectable_objects.discard(selectable_object)

    def is_hovered(self, mouse_pos):
        return next((selectable_object for selectable_object in self.selectable_objects if selectable_object.is_hovered(mouse_pos)), None)

    def select_object(self, selected_object):
        self.selected_object = selected_object

    def get_selected_object(self):
        return self.selected_object

    def update(self, selectable_object):
        self.remove_selectable_object(selectable_object)

    def reset(self, game_world):
        self.game_world = game_world
        self.selected_object = None
        self.selectable_objects = set()
        self.register_selectable_objects()
