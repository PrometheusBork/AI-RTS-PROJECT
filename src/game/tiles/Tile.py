import pygame

from game.interfaces.IHoverable import IHoverable
from game.interfaces.IObserveable import IObserveable
from game.interfaces.IRenderable import IRenderable
from game.objects.GameObject import GameObject


class Tile(pygame.sprite.Sprite, IHoverable, IRenderable, IObserveable):
    def __init__(self, position=(0, 0)):
        super().__init__()
        self.position = position
        self.tile_size = 50
        self.image = pygame.Surface([self.tile_size, self.tile_size])
        self.rect = self.image.get_rect(topleft=(self.position[1] * self.tile_size + self.tile_size, self.position[0] * self.tile_size + self.tile_size))
        self.is_walkable = False
        self.game_object = None
        self._observers = []
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
        if not self.is_empty():
            self.game_object = None
        elif self.is_empty():
            print('Tried to remove game object from a empty tile at', self.position)

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
        return False

    def get_debug_info(self):
        return f'({self.position[0]}, {self.position[1]})\n{self.is_walkable and self.is_empty()}'

    def get_render_priority(self):
        return 1

    @property
    def observers(self):
        return self._observers

    def register(self, observer):
        self._observers.append(observer)

    def unregister(self, observer):
        self._observers.remove(observer)

    def notify(self, data=None):
        for observer in self._observers:
            observer.update(data)
