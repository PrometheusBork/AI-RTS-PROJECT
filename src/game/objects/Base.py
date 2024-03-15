import pygame

from game.objects.GameObject import GameObject


class Base(GameObject):
    def __init__(self, health=100):
        super().__init__()
        self.health = health
        self.image = pygame.transform.scale(pygame.image.load('src/game/assets/base.png'), (50, 50))
        self.rect = pygame.Rect(self.col * 50 + 50, self.row * 50 + 50, 50, 50)

    def add_health(self, health):
        self.health += health
