import pygame

from src.game.interfaces.IObserver import IObserver
from src.game.interfaces.IObserveable import IObserveable


class SpriteManager(IObserver):
    def __init__(self, game_world):
        self.sprite_groups = {}
        self.game_world = game_world
        self.register_sprite_groups()

    def register_sprite_groups(self):
        for row in self.game_world.map:
            for tile in row:
                self.add_sprite(tile)
                if not tile.is_empty():
                    self.add_sprite(tile.game_object)

        # Sort the sprite groups by render priority
        self.sort_sprite_groups()

    def add_sprite(self, sprite):
        sprite_type = type(sprite)

        # If the sprite group does not exist, create the sprite group and add sprite
        # If the sprite group does exist, skips the creation of the sprite group but still add the sprite
        self.sprite_groups.setdefault(sprite_type, pygame.sprite.Group()).add(sprite)

        if isinstance(sprite, IObserveable):
            sprite.register(self)
        return self

    def remove_sprite(self, sprite):
        sprite_type = type(sprite)
        if sprite_type in self.sprite_groups:
            self.sprite_groups[sprite_type].remove(sprite)

    def get_sprite_group(self, sprite_type):
        return self.sprite_groups.get(sprite_type, {})
        
    def sort_sprite_groups(self):
        self.sprite_groups = {t: self.sprite_groups[t] for t in sorted(self.sprite_groups, key=lambda x: x().get_render_priority())}

    def update(self, destroyed_object):
        self.remove_sprite(destroyed_object)

    def reset(self, game_world):
        self.game_world = game_world
        self.sprite_groups = {}
        self.register_sprite_groups()
