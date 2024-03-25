from enum import Enum


class GameState(Enum):
    QUIT = 0
    MENU = 1
    RUNNING = 2
    PAUSED = 3
