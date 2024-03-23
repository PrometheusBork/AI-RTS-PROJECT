import pygame

from game.tiles.Tile import Tile


class WaterTile(Tile):
    def __init__(self, position=(0, 0)):
        super().__init__(position)
        self.image = pygame.transform.scale(pygame.image.load('src/game/assets/water_tile.png'), (self.tile_size, self.tile_size))
        self.is_walkable = False
