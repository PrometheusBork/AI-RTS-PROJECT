class Tile:
    def __init__(self, row, col):
        self.tile_type = None
        self.row = row
        self.col = col
        self.game_objects = []
        self.is_walkable = False

    def add_game_object(self, game_object):
        self.game_objects.append(game_object)

    def remove_game_object(self, game_object):
        self.game_objects.remove(game_object)

    def is_empty(self):
        return len(self.game_objects) == 0
