from game.GameEngine import GameEngine
from game.GameRender import GameRender
from game.maps.Map import Map
from game.units.WorkerUnit import WorkerUnit
from game.units.InfantryUnit import InfantryUnit

map_name = input("Enter the map name: ")
if map_name not in Map.maps:
    print("No map name entered, using default map")
    map_name = "map1"

grid_size = (10, 10) # We should find a way to get the Grid Size from the Map file
tile_size = 50
screen_size = (grid_size[0] * tile_size + (2 * tile_size) + 200, grid_size[1] * tile_size + (2 * tile_size))

# Create a GameWorld instance
game_world = Map.map(map_name)

game_world.map[2][2].add_game_object(WorkerUnit(position=(2, 2)))
game_world.map[3][1].add_game_object(InfantryUnit(position=(3, 1)))


# Create Game Render instance
game_render = GameRender(game_world, screen_size, grid_size, tile_size)

# Create Game Engine instance
game_engine = GameEngine(game_world, game_render)

# Start the game loop
game_engine.run()
