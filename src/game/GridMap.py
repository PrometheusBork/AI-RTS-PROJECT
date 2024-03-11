import pygame

from src.game.tiles.Tile import Tile


class GridMap:
    def __init__(self, grid_size=12, tick_rate=12):
        self.window = pygame.init()
        self.window = pygame.display.set_mode((grid_size * 32 + 250, grid_size * 32 + 64))
        self.grid_size = grid_size
        self.clock = pygame.time.Clock()
        self.clock.tick(tick_rate)
        self.map = [[Tile(row, col) for col in range(self.grid_size)] for row in range(self.grid_size)]

    def draw(self):
        self.__draw_grid()
        pygame.display.flip()

    def __draw_grid(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                self.map[row][col].draw(self.window)
