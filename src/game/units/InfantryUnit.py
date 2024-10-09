import pygame

from src.game.interfaces.IAttacker import IAttacker
from src.game.units.Unit import Unit


class InfantryUnit(Unit, IAttacker):
    def __init__(self):
        super().__init__("Infantry", 40)
        self.image = pygame.transform.scale(pygame.image.load('src/game/assets/infantry.png'), (40, 40))
        self.rect = self.image.get_rect()
        self._damage = 10

    def update(self, game_world):
        pass

    @property
    def damage(self):
        return self._damage

    def attack(self, target):
        target.take_damage(self.damage)
