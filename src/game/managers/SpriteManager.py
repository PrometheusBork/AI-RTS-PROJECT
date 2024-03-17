import pygame


class SpriteManager:
    def __init__(self):
        self.sprite_groups = {}

    def register_sprite_group(self, sprite_type):
        if sprite_type not in self.sprite_groups:
            self.sprite_groups[sprite_type] = pygame.sprite.Group()

    def add_sprite(self, sprite):
        sprite_type = type(sprite)
        self.register_sprite_group(sprite_type)
        self.sprite_groups[sprite_type].add(sprite)

    def get_sprite_group(self, sprite_type):
        if sprite_type in self.sprite_groups:
            return self.sprite_groups[sprite_type]
        else:
            return None
