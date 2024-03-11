import pygame.font
import pygame


class Tile:
    def __init__(self, row, col):
        self.TileType = None
        self.row = row
        self.col = col
        self.width = 32
        self.height = 32
        self.color = (0, 255, 0)
        self.isWalkable = True
        self.font = pygame.font.SysFont('arial', 12)
        self.label = str(row) + ',' + str(col)
        self.text = self.font.render(self.label, True, (0, 0, 0))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (32 + self.row * self.width + 1, 32 + self.col * self.height + 1, self.width - 1, self.height - 1))
        screen.blit(self.text, (32 + self.row * self.width + 1, 32 + self.col * self.height + 1))
