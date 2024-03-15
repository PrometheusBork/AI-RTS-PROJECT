import pygame


class GameObject(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.row = 0
        self.col = 0
        self.image = None
        self.rect = None

    def update_position(self, row, col):
        self.row = row
        self.col = col
        self.rect = (self.col * 50 + 50, self.row * 50 + 50)
