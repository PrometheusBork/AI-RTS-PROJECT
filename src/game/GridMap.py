from game.tiles.Tile import Tile

from game.tiles.GrassTile import GrassTile


class GridMap:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.map = self.__create_void_plane()

    def __create_void_plane(self):
        return [[Tile((row, col)) for col in range(self.grid_size[1])] for row in range(self.grid_size[0])]

    def create_grass_plane(self):
        self.map = [[GrassTile((row, col)) for col in range(self.grid_size[1])] for row in range(self.grid_size[0])]
        return self

    def set_tile(self, position, tile):
        self.map[position[0]][position[1]] = tile
        self.map[position[0]][position[1]].update_position(position)

    def set_game_object(self, position, game_object):
        if position[0] < self.grid_size[0] and position[1] < self.grid_size[1]:
            self.map[position[0]][position[1]].add_game_object(game_object)
        else:
            print('Tried to add', game_object, 'to a non-existing tile at', position)
