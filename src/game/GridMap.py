from src.game.managers.PlayerManager import PlayerManager
from src.game.tiles.Tile import Tile
from src.game.tiles.GrassTile import GrassTile


class GridMap:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.map = self.__create_void_plane()
        self.player_manager = PlayerManager()

    def __create_void_plane(self):
        return [[Tile((row, col)) for col in range(self.grid_size[1])] for row in range(self.grid_size[0])]

    def create_grass_plane(self):
        self.map = [[GrassTile((row, col)) for col in range(self.grid_size[0])] for row in range(self.grid_size[0])]
        return self

    def set_tile(self, position, tile):
        self.map[position[0]][position[1]] = tile
        self.map[position[0]][position[1]].set_position(position)

    def get_tile(self, position):
        return self.map[position[0]][position[1]]

    def is_position_out_of_bounds(self, position):
        return position[0] < 0 or position[1] < 0 or position[0] >= self.grid_size[0] or position[1] >= self.grid_size[1]

    def set_game_object(self, position, game_object):
        if not self.is_position_out_of_bounds(position):
            self.get_tile(position).add_placeable_object(game_object)
        else:
            print('Tried to add', game_object, 'to a non-existing tile at', position)
    
    def remove_game_object(self, position):
        if not self.is_position_out_of_bounds(position):
            self.get_tile(position).remove_placeable_object()
        else:
            print('Tried to remove game object at', position)

    def clear_objects(self):
        for row in self.map:
            for tile in row:
                if not tile.is_empty():
                    tile.remove_placeable_object()
