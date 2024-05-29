import pygame

from src.game.interfaces.IAttackable import IAttackable
from src.game.interfaces.IMoveable import IMovable
from src.game.objects.GameObject import GameObject


class Unit(GameObject, IAttackable, IMovable):
    def __init__(self, name, health):
        super().__init__()
        self.name = name
        self._health = health
        self.image = pygame.Surface((50, 50))
        self.color_image = pygame.Surface(self.image.get_size()).convert_alpha()
        self.image.blit(self.color_image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.rect = self.image.get_rect()
        self._observers = set()

    @property
    def health(self):
        return self._health

    def set_color(self):
        self.image.blit(self.color_image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

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

    def take_damage(self, damage):
        self._health -= damage
        if self.is_destroyed():
            self._health = 0
            self.notify(self)

    def is_destroyed(self):
        return self._health <= 0

    def __str__(self):
        return f'{self.name} has {self.health} health'

    def get_render_priority(self):
        return 1

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
