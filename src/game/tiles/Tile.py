class Tile:
    def __init__(self, row, col):
        self.tile_type = None
        self.row = row
        self.col = col
        self.game_object = None
        self.is_walkable = False

    def add_game_object(self, game_object):
        if self.is_empty():
            self.game_object = game_object
        else: 
            print("Game object already exists in this tile")

    def remove_game_object(self):
        self.game_object = None

    def is_empty(self):
        return self.game_object is None
