from game.GameEngine import GameEngine
from game.GameRender import GameRender
from game.maps.Map import Map

map_name = input("Enter the map name: ")
if map_name not in Map.maps:
    print("No map name entered, using default map")
    map_name = "map1"

grid_size = (10, 10) # We should find a way to get the Grid Size from the Map file
tile_size = 50
screen_size = (grid_size[0] * tile_size + (2 * tile_size) + 200, grid_size[1] * tile_size + (2 * tile_size))

# Create a GameWorld instance
game_world = Map.map(map_name)

# Create Game Render instance
game_render = GameRender(screen_size, grid_size, tile_size)

# Create Game Engine instance
game_engine = GameEngine(game_world, game_render)

# Start the game loop
game_engine.run()
