import pygame

from abstracts.BaseTile import BaseTile
from interfaces.IHoverable import IHoverable
from interfaces.IRenderable import IRenderable
from objects.GameObject import GameObject


class Tile(BaseTile, IHoverable, IRenderable):
    def __init__(self, position=(0, 0)):
        super().__init__()
        self.position = position
        self.tile_size = 50
        self.image = pygame.Surface([self.tile_size, self.tile_size])
        self.rect = self.image.get_rect(topleft=(self.position[1] * self.tile_size + self.tile_size, self.position[0] * self.tile_size + self.tile_size))
        self.is_walkable = False
        self.game_object = None
        pygame.draw.rect(self.image, (255, 255, 255), (0, 0, self.tile_size, self.tile_size), 1)

    def set_position(self, position):
        self.position = position
        self.rect = pygame.Rect(self.position[1] * self.tile_size + self.tile_size, self.position[0] * self.tile_size + self.tile_size, self.tile_size, self.tile_size)

    def add_placeable_object(self, placeable_object):
        if self.is_empty() and isinstance(placeable_object, GameObject):
            self.game_object = placeable_object
            self.game_object.set_position((self.position[0], self.position[1]))
        elif not self.is_empty() and isinstance(placeable_object, GameObject):
            print('Tried to add', placeable_object, 'to a non-empty tile at', self.position)
        else:
            raise 'Tried to add a non-GameObject to a tile'

    def remove_placeable_object(self):
        self.game_object = None

    def is_empty(self):
        return self.game_object is None

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def render_hover(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)

    def get_hover_priority(self):
        return 2

    def get_sprite_group(self):
        return pygame.sprite.Group([self])

    def has_debug_info(self):
        return True

    def get_debug_info(self):
        return f'({self.position[0]}, {self.position[1]})\n{self.is_walkable}'

    def get_render_priority(self):
        return 1
