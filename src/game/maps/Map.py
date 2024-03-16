from game.GridMap import GridMap
from game.objects.Tree import Tree
from game.objects.Base import Base
from game.tiles.StoneTile import StoneTile
from game.tiles.WaterTile import WaterTile
from game.units.WorkerUnit import WorkerUnit
from game.units.InfantryUnit import InfantryUnit


class Map:
    maps = ["map1", "map2", "map3"]

    def select_map(self):
        if self == "map1":
            # Create a GameWorld instance
            game_world = GridMap((10, 10))

            # Map
            game_world.create_grass_plane()

            game_world.set_tile((5, 6), WaterTile())
            game_world.set_tile((5, 7), WaterTile())
            game_world.set_tile((4, 6), WaterTile())
            game_world.set_tile((4, 7), WaterTile())
            game_world.set_tile((3, 2), StoneTile())
            game_world.set_tile((3, 3), StoneTile())
            game_world.set_tile((3, 4), StoneTile())
            game_world.set_tile((2, 3), StoneTile())

            # Game Objects
            game_world.set_game_object((0, 0), Base())
            game_world.set_game_object((9, 9), Base())
            game_world.set_game_object((7, 1), Tree())
            game_world.set_game_object((7, 2), Tree())
            game_world.set_game_object((6, 2), Tree())
            game_world.set_game_object((7, 7), Tree())
            game_world.set_game_object((0, 8), Tree())
            game_world.set_game_object((0, 9), Tree())
            game_world.set_game_object((1, 9), Tree())
            game_world.set_game_object((3, 7), Tree())
            game_world.set_game_object((1, 4), Tree())
            game_world.set_game_object((9, 5), Tree())
            return game_world
        elif self == "map2":
            return GridMap((10, 10)).create_grass_plane()
