from src.game.GameLoop import GameLoop
from src.game.GridMap import GridMap

game = GridMap(grid_size=12)

loop = GameLoop(game)
loop.start()
