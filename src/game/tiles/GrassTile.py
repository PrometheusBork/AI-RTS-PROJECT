import pygame

from game.tiles.Tile import Tile


class GrassTile(Tile):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.image = pygame.transform.scale(pygame.image.load('src/game/assets/base.png'), (50, 50))
        self.rect = pygame.Rect(self.col * 50 + 50, self.row * 50 + 50, 50, 50)
        self.tile_type = "Grass"
        self.is_walkable = True
        self.colorImage = pygame.Surface(self.image.get_size())
        self.colorImage.fill((0, 255, 0))
        self.image.blit(self.colorImage, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    def update(self):
        pass
