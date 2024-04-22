import pygame

from game.interfaces.ICollectable import ICollectable
from game.objects.GameObject import GameObject


class Tree(GameObject, ICollectable):
    def __init__(self, health=100, resources=1000):
        super().__init__()
        self._health = health
        self._resources = resources
        self.image = pygame.transform.scale(pygame.image.load('src/game/assets/tree.png'), (20, 60))
        self.rect = self.image.get_rect()
        self._observers = set()

    @property
    def health(self):
        return self._health

    def get_resource(self, resources=100):
        self._resources -= resources
        self.take_damage(resources)
        return resources

    def take_damage(self, damage):
        self._health -= damage
        if self.is_destroyed():
            self._health = 0
            self.notify(self)

    def is_destroyed(self):
        return self._health <= 0

    def set_position(self, position):
        row, col = position
        self.rect.centerx = col * 50 + 50 // 2 + 50
        self.rect.bottom = row * 50 + 50 // 2 + 50

    def get_render_priority(self):
        return 3

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
