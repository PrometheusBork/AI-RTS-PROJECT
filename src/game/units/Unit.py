import pygame

from interfaces.IAttackable import IAttackable
from interfaces.IMoveable import IMovable
from objects.GameObject import GameObject


class Unit(GameObject, IAttackable, IMovable):
    def __init__(self, name, health, damage):
        super().__init__()
        self.name = name
        self._health = health
        self.damage = damage
        self.image = pygame.transform.scale(pygame.image.load('src/game/assets/base.png'), (40, 40))
        self.rect = self.image.get_rect()

    @property
    def health(self):
        return self._health

    def get_position(self):
        return self.row, self.col

    def set_position(self, position):
        row, col = position
        self.row = row
        self.col = col
        self.rect.centerx = col * 50 + 50 // 2 + 50
        self.rect.centery = row * 50 + 50 // 2 + 50

    def update_position(self, new_position):
        self.set_position(new_position)

    def attack(self, target):
        target.health -= self.damage

    def take_damage(self, damage):
        self._health -= damage
        if self._health < 0:
            self._health = 0

    def is_destroyed(self):
        return self._health <= 0

    def __str__(self):
        return f'{self.name} has {self.health} health and {self.damage} damage'
