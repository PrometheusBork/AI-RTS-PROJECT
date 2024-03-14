from game.tiles.Tile import Tile


class StoneTile(Tile):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.tile_type = "Stone"
        self.is_walkable = False
