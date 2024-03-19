import pygame

from game.tiles.Tile import Tile


class GrassTile(Tile):
    def __init__(self, position=(0, 0)):
        super().__init__(position)
        self.image = pygame.transform.scale(pygame.image.load('src/game/assets/grass_tile.png'), (self.tile_size, self.tile_size))
        self.is_walkable = True
