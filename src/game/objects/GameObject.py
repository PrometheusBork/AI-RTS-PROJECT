import pygame

from game.abstracts.BaseGameObject import BaseGameObject
from game.interfaces.IRenderable import IRenderable
from game.interfaces.ISelectable import ISelectable


class GameObject(BaseGameObject, IRenderable, ISelectable):
    def __init__(self):
        super().__init__()
        self.row = 0
        self.col = 0
        self.image = pygame.Surface([50, 50])
        self.rect = self.image.get_rect()

    def set_position(self, position):
        self.row, self.col = position
        self.rect = pygame.Rect(self.col * 50 + 50, self.row * 50 + 50, 50, 50)

    def render_hover(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def get_hover_priority(self):
        return 1

    def get_sprite_group(self):
        return pygame.sprite.Group([self])

    def has_debug_info(self):
        return False

    def get_debug_info(self):
        return ''
