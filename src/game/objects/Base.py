import pygame

from src.game.interfaces.IAttackable import IAttackable
from src.game.objects.GameObject import GameObject


class Base(GameObject, IAttackable):
    def __init__(self, health=100):
        super().__init__()
        self._health = health
        self.image = pygame.transform.scale(pygame.image.load('src/game/assets/base.png'), (40, 40))
        self.rect = self.image.get_rect()
        self._observers = set()

    @property
    def health(self):
        return self._health

    def take_damage(self, damage):
        self._health -= damage
        if self.is_destroyed():
            self._health = 0
            self.notify(self)

    def is_destroyed(self):
        return self._health <= 0

    def set_position(self, position):
        self.row, self.col = position
        self.rect.centerx = self.col * 50 + 50 // 2 + 50
        self.rect.centery = self.row * 50 + 50 // 2 + 50

    def get_render_priority(self):
        return 2

    @property
    def observers(self):
        return self._observers

    def register(self, observer):
        self._observers.add(observer)

    def unregister(self, observer):
        self._observers.discard(observer)

    def notify(self, data=None):
        for observer in self._observers:
            observer.update(data)
