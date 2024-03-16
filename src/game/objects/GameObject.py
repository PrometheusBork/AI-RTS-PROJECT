import pygame

from interfaces.IHoverable import IHoverable


class GameObject(pygame.sprite.Sprite, IHoverable):
    def __init__(self):
        super().__init__()
        self.row = 0
        self.col = 0
        self.image = pygame.Surface([50, 50])
        self.rect = self.image.get_rect()

    def update_position(self, row, col):
        self.row = row
        self.col = col
        self.rect = pygame.Rect(self.col * 50 + 50, self.row * 50 + 50, 50, 50)

    def render_hover(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
