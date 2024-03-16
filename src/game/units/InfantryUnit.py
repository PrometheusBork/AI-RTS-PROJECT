import pygame

from game.units.Unit import Unit


class InfantryUnit(Unit):
    def __init__(self):
        super().__init__("Infantry", 100, 10)
        self.image = pygame.transform.scale(pygame.image.load('src/game/assets/Red.PNG'), (50, 50))

    def update(self, game_world):
        pass
