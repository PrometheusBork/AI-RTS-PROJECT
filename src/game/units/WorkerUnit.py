import pygame
from game.units.Unit import Unit

class WorkerUnit(Unit):
    def __init__(self, position):
        super().__init__("Worker", 100, 1, position)
        self.sprite = pygame.image.load('src/game/assets/WorkerUnit.png') # Inefficient to load the image every time a tree is created
        self.scaled_sprite = pygame.transform.scale(self.sprite, (40, 40))
        self.rect = self.scaled_sprite.get_rect()
    
    def collect(self, resource): # Not implemented yet
        #resource.collect(10)
        pass
    
    def update(self, game_world):
        pass

    def render(self, game_render):
        tile_rect = pygame.Rect(self.position[1] * game_render.tile_size + game_render.tile_size, self.position[0] * game_render.tile_size + game_render.tile_size,
                                        game_render.tile_size, game_render.tile_size)
        self.rect.center = tile_rect.center
        game_render.screen.blit(self.scaled_sprite.convert_alpha(), self.rect)