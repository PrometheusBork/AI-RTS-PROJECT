import pygame

from game.tiles.Tile import Tile


class StoneTile(Tile):
    def __init__(self, position=(0, 0)):
        super().__init__(position)
        self.image = pygame.transform.scale(pygame.image.load('game/assets/stone_tile.png'), (self.tile_size, self.tile_size))
        self.is_walkable = False
