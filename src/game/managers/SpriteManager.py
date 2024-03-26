import pygame

from game.interfaces.IObserver import IObserver
from game.interfaces.IObserveable import IObserveable


class SpriteManager(IObserver):
    def __init__(self):
        self.sprite_groups = {}

    def register_sprite_group(self, sprite_type):
        if sprite_type not in self.sprite_groups:
            self.sprite_groups[sprite_type] = pygame.sprite.Group()

            # Sort the sprite groups by render priority
            self.sprite_groups = {t: self.sprite_groups[t] for t in sorted(self.sprite_groups, key=lambda x: x().get_render_priority())}

    def add_sprite(self, sprite):
        sprite_type = type(sprite)
        self.register_sprite_group(sprite_type)
        self.sprite_groups[sprite_type].add(sprite)
        if isinstance(sprite, IObserveable):
            sprite.register(self)

    def remove_sprite(self, sprite):
        sprite_type = type(sprite)
        if sprite_type in self.sprite_groups:
            self.sprite_groups[sprite_type].remove(sprite)

    def get_sprite_group(self, sprite_type):
        if sprite_type in self.sprite_groups:
            return self.sprite_groups[sprite_type]
        else:
            return None

    def update(self, destroyed_object):
        self.remove_sprite(destroyed_object)
