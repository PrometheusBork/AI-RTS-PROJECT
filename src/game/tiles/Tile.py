import pygame

from interfaces.IHoverable import IHoverable
from observers.HoverObserver import HoverObserver


class Tile(pygame.sprite.Sprite, IHoverable):
    def __init__(self, position=(0, 0)):
        super().__init__()
        self.position = position
        self.tile_size = 50
        self.image = pygame.Surface([self.tile_size, self.tile_size])
        self.rect = self.image.get_rect(topleft=(self.position[1] * self.tile_size + self.tile_size, self.position[0] * self.tile_size + self.tile_size))
        self.is_walkable = False
        self.game_object = None
        pygame.draw.rect(self.image, (255, 255, 255), (0, 0, self.tile_size, self.tile_size), 1)

    def update_position(self, new_position):
        self.position = new_position
        self.rect = pygame.Rect(self.position[1] * self.tile_size + self.tile_size, self.position[0] * self.tile_size + self.tile_size, self.tile_size, self.tile_size)

    def add_game_object(self, game_object):
        if self.is_empty():
            self.game_object = game_object
            self.game_object.update_position(self.position[0], self.position[1])
        else:
            print('Tried to add', game_object, 'to a non-empty tile at', self.position)

    def remove_game_object(self):
        self.game_object = None

    def is_empty(self):
        return self.game_object is None

    def render_hover(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
