from game.GridMap import GridMap
from game.objects.Tree import Tree
from game.objects.Base import Base
from game.tiles.StoneTile import StoneTile
from game.tiles.WaterTile import WaterTile
from game.units.WorkerUnit import WorkerUnit
from game.units.InfantryUnit import InfantryUnit
from game.players.Player import Player
from game.managers.PlayerManager import PlayerManager


class Map:
    maps = ["map1", "map2", "map3"]
    def select_map(self):
        if self == "map1":
            # Create a GameWorld instance
            game_world = GridMap((10, 10))

            # Create Player instances
            player1 = Player(100, Base())
            player2 = Player(100, Base())

            game_world.player_manager.add_player(player1)
            game_world.player_manager.add_player(player2)
            
            player1.add_unit(WorkerUnit())
            player1.add_unit(WorkerUnit())
            player2.add_unit(InfantryUnit())

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
            game_world.set_game_object((0, 0), player1.base)
            game_world.set_game_object((9, 9), player2.base)
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
            game_world.set_game_object((2, 2), player1.units[0])
            game_world.set_game_object((9, 8), player2.units[0])
            return game_world
        elif self == "map2":
            return GridMap((10, 10)).create_grass_plane()
