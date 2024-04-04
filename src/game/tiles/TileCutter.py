import pygame

class SpriteSheet:
    def __init__(self,file):
        self.sheet = pygame.image.load(file).pygame.Surface.convert()
        self.terrain_spritesheet = SpriteSheet('src\game\assets\terrainSpriteSheet.png')

        def get_sprite(self, x, y, width, height):
            sprite = pygame.Surface([width, height])
            sprite.blit(self.sheet, (0,0), (x, y, width, height))
            sprite.set_colorkey(255,255)
            return sprite