import pygame
from game.units.Unit import Unit


class WorkerUnit(Unit):
    def __init__(self):
        super().__init__("Worker", 100, 1)
        self.image = pygame.transform.scale(pygame.image.load('src/game/assets/WorkerUnit.png'), (50, 50))

    def collect(self, resource):  # Not implemented yet
        # resource.collect(10)
        pass

    def update(self, game_world):
        pass
