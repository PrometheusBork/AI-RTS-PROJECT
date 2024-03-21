import pygame
from game.units.Unit import Unit
from game.interfaces.ICollect import ICollect


class WorkerUnit(Unit, ICollect):
    def __init__(self):
        super().__init__("Worker", 100, 1)
        self.image = pygame.transform.scale(pygame.image.load('src/game/assets/WorkerUnit.png'), (40, 40))
        self.rect = self.image.get_rect()

    def update(self, game_world):
        pass

    def collect(self, game_world):
        print("Worker is collecting resources")
        for player in game_world.players:
            for player_unit in player.units:
                if player_unit == self:
                    player.add_resources(10)
                    return