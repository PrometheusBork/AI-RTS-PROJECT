import pygame

from game.interfaces.IAttackable import IAttackable
from game.objects.GameObject import GameObject


class Tree(GameObject, IAttackable):
    def __init__(self, health=100):
        super().__init__()
        self._health = health
        self.image = pygame.transform.scale(pygame.image.load('src/game/assets/tree.png'), (20, 60))
        self.rect = self.image.get_rect()

    @property
    def health(self):
        return self._health

    def take_damage(self, damage):
        self._health -= damage
        if self._health < 0:
            self._health = 0

    def is_destroyed(self):
        return self._health <= 0

    def set_position(self, position):
        row, col = position
        self.rect.centerx = col * 50 + 50 // 2 + 50
        self.rect.bottom = row * 50 + 50 // 2 + 50

    def get_render_priority(self):
        return 3
