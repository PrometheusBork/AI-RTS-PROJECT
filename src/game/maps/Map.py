from game.GridMap import GridMap
from game.objects.Tree import Tree
from game.objects.Base import Base
from game.tiles.GrassTile import GrassTile
from game.tiles.StoneTile import StoneTile
from game.tiles.WaterTile import WaterTile
from game.units.WorkerUnit import WorkerUnit
from game.units.InfantryUnit import InfantryUnit

class Map:
    def map(map_name):
        match map_name:
            case "map1":
                grid_size = (10, 10)

                # Create a GameWorld instance
                game_world = GridMap(grid_size)

                # Map
                for row in range(0, 10):
                    for col in range(0, 10):
                        tile = GrassTile(row, col)
                        game_world.map[row][col] = tile            

                game_world.map[5][6] = WaterTile(5, 6)
                game_world.map[5][5] = WaterTile(5, 5)
                game_world.map[4][6] = WaterTile(4, 6)
                game_world.map[4][7] = WaterTile(4, 7)
                game_world.map[3][2] = StoneTile(3, 2)
                game_world.map[3][3] = StoneTile(3, 3)
                game_world.map[3][4] = StoneTile(3, 4)
                game_world.map[2][3] = StoneTile(2, 3)

            # Game Objects
                game_world.map[0][0].add_game_object(Base(position=(0, 0)))
                game_world.map[9][9].add_game_object(Base(position=(9, 9)))
                game_world.map[2][2].add_game_object(WorkerUnit(position=(2, 2)))
                game_world.map[3][1].add_game_object(InfantryUnit(position=(3, 1)))
                game_world.map[7][1].add_game_object(Tree(position=(7, 1)))
                game_world.map[7][2].add_game_object(Tree(position=(7, 2)))
                game_world.map[6][2].add_game_object(Tree(position=(6, 2)))
                game_world.map[7][7].add_game_object(Tree(position=(7, 7)))
                game_world.map[0][8].add_game_object(Tree(position=(0, 8)))
                game_world.map[0][9].add_game_object(Tree(position=(0, 9)))
                game_world.map[1][9].add_game_object(Tree(position=(1, 9)))
                game_world.map[3][7].add_game_object(Tree(position=(3, 7)))
                game_world.map[1][4].add_game_object(Tree(position=(1, 4)))
                game_world.map[9][5].add_game_object(Tree(position=(9, 5)))
                return game_world
            case "map2":
                grid_size = (10, 10)
                
                # Create a GameWorld instance
                game_world = GridMap(grid_size)
                
                # Map
                for row in range(0, 10):
                    for col in range(0, 10):
                        tile = GrassTile(row, col)
                        game_world.map[row][col] = tile
                return game_world
