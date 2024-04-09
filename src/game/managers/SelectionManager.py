from game.interfaces.ISelectable import ISelectable

class SelectionManager:
    def __init__(self, game_world):
        self.game_world = game_world
        self.selectable_object = []
        self.selected_object = None

    def register_selectable_objects(self):
        for row in self.game_world.map:
            for tile in row:
                if not tile.is_empty():
                    self.add_selectable_object(tile.game_object)
                    
    def add_selectable_object(self, selectable_object):
        if isinstance(selectable_object, ISelectable):
            self.selectable_object.append(selectable_object)

    def is_hovered(self, mouse_pos):
        for selectable_object in self.selectable_object:
            if selectable_object.is_hovered(mouse_pos):
                return selectable_object
        return None

    def select_object(self, selected_object):
        if selected_object is None:
            self.selected_object = None
            return None
        else: 
            self.selected_object = selected_object
            return self.selected_object

    def get_selected_object(self):
        return self.selected_object