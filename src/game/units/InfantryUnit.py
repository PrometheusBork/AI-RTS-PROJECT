import pygame
from game.units.Unit import Unit

class InfantryUnit(Unit):
    def __init__(self, position):
        super().__init__("Infantry", 100, 10, position)
        self.sprite = pygame.image.load('src/game/assets/Red.PNG') # Inefficient to load the image every time a tree is created
        self.scaled_sprite = pygame.transform.scale(self.sprite, (40, 40))
        self.rect = self.scaled_sprite.get_rect()
    
    def update(self, game_world):
        pass

    def render(self, game_render):
        tile_rect = pygame.Rect(self.position[1] * game_render.tile_size + game_render.tile_size, self.position[0] * game_render.tile_size + game_render.tile_size,
                                        game_render.tile_size, game_render.tile_size)
        self.rect.center = tile_rect.center
        game_render.screen.blit(self.scaled_sprite.convert_alpha(), self.rect)