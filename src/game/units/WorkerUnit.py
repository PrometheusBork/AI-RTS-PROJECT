import pygame
from game.units.Unit import Unit


class WorkerUnit(Unit):
    def __init__(self):
        super().__init__("Worker", 100, 1)
        self.image = pygame.transform.scale(pygame.image.load('src/game/assets/WorkerUnit.png'), (40, 40))
        self.rect = self.image.get_rect()

    def collect(self, resources):  # Not implemented yet. Maybe implement as interface instead
        #resources += 10 # Dont know if this is right either purely pseudo
        #return resources
        pass

    def update(self, game_world):
        pass
