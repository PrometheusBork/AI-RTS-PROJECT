import pygame

from game.objects.GameObject import GameObject


class Base(GameObject):
    def __init__(self, position, health=100):
        super().__init__(position)
        self.health = health
        self.sprite = pygame.image.load('src/game/assets/base.png') # Inefficient to load the image every time a base is created
        self.scaled_sprite = pygame.transform.scale(self.sprite, (40, 40))
        self.rect = self.scaled_sprite.get_rect()

    def update(self, game_world):
        pass

    def render(self, game_render):
        tile_rect = pygame.Rect(self.position[1] * game_render.tile_size + game_render.tile_size, self.position[0] * game_render.tile_size + game_render.tile_size,
                                        game_render.tile_size, game_render.tile_size)
        self.rect.center = tile_rect.center
        game_render.screen.blit(self.scaled_sprite.convert_alpha(), self.rect)