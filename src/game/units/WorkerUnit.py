import pygame
from src.game.units.Unit import Unit
from src.game.interfaces.ICollector import ICollector


class WorkerUnit(Unit, ICollector):
    def __init__(self):
        super().__init__("Worker", 100)
        self.image = pygame.transform.scale(pygame.image.load('src/game/assets/WorkerUnit.png'), (40, 40))
        self.rect = self.image.get_rect()

    def collect(self, collectable_object):
        return collectable_object.get_resource(25)

    def update(self, game_world):
        pass
