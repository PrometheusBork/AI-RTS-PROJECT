from src.game.tiles.Tile import Tile


class GrassTile(Tile):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.tile_type = "Grass"
        self.is_walkable = True
