from game.tiles.Tile import Tile


class WaterTile(Tile):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.tile_type = "Water"
        self.is_walkable = False
