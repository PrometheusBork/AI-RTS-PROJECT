from game.GameEngine import GameEngine
from game.GridMap import GridMap
from game.GameRender import GameRender
from game.objects.Tree import Tree
from game.objects.Base import Base
from game.tiles.GrassTile import GrassTile
from game.tiles.WaterTile import WaterTile

grid_size = (10, 10)
tile_size = 50
screen_size = (grid_size[0] * tile_size + (2 * tile_size) + 200, grid_size[1] * tile_size + (2 * tile_size))

# Create a GameWorld instance
game_world = GridMap(grid_size)

# Map
for row in range(0, 10):
    for col in range(5):
        tile = GrassTile(row, col)
        game_world.map[row][col] = tile
    game_world.map[row][1].add_game_object(Tree(position=(row, 1)))
    game_world.map[row][0].add_game_object(Base(position=(row, 0)))

print(game_world.map[1][0].game_object) # Can be deleted, is just used for checking what object is on the tile

for row in range(0, 10):
    for col in range(5, 10):
        tile = WaterTile(row, col)
        game_world.map[row][col] = tile

# Create Game Render instance
game_render = GameRender(screen_size, grid_size, tile_size)

# Create Game Engine instance
game_engine = GameEngine(game_world, game_render)

# Start the game loop
game_engine.run()
