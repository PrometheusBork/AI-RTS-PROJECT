import pygame

from units.Unit import Unit


class InfantryUnit(Unit):
    def __init__(self):
        super().__init__("Infantry", 100, 10)
        self.image = pygame.transform.scale(pygame.image.load('src/game/assets/Red.PNG'), (40, 40))
        self.rect = self.image.get_rect()

    def update(self, game_world):
        pass
