import pygame

from game.objects.GameObject import GameObject


class Base(GameObject):
    def __init__(self, health=100):
        super().__init__()
        self.health = health
        self.image = pygame.transform.scale(pygame.image.load('src/game/assets/base.png'), (40, 40))
        self.rect = self.image.get_rect()

    def update_position(self, row, col):
        self.row = row
        self.col = col
        self.rect.centerx = col * 50 + 50 // 2 + 50
        self.rect.centery = row * 50 + 50 // 2 + 50

    def add_health(self, health):
        self.health += health
