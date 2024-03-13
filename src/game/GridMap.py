from game.tiles.Tile import Tile


class GridMap:
    def __init__(self, grid_size):
        self.map = [[Tile(row, col) for col in range(grid_size[1])] for row in range(grid_size[0])]
