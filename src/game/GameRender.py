import pygame
import psutil

from game.objects.Tree import Tree
from game.objects.Base import Base
from game.tiles.GrassTile import GrassTile
from game.tiles.WaterTile import WaterTile

DEBUG_MODE = True
process = psutil.Process()


class GameRender:
    def __init__(self, game_world, screen_size, grid_size, tile_size):
        pygame.init()
        self.screen_size = screen_size
        self.grid_size = (len(game_world.map), len(game_world.map[0]))
        self.tile_size = tile_size
        self.base_group = pygame.sprite.Group()
        self.tree_group = pygame.sprite.Group()
        self.grid_group = pygame.sprite.Group()

        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("Game")

        self.font = pygame.font.SysFont('Arial', 12)
        self.clock = pygame.time.Clock()

        for row in range(self.grid_size[0]):
            for col in range(self.grid_size[1]):
                tile = game_world.map[row][col]
                self.grid_group.add(tile)
                if not tile.is_empty():
                    if isinstance(tile.game_object, Tree):
                        self.tree_group.add(tile.game_object)
                    elif isinstance(tile.game_object, Base):
                        self.base_group.add(tile.game_object)

    def render(self, game_world):
        self.screen.fill((0, 0, 0))
        self.grid_group.draw(self.screen)
        self.tree_group.draw(self.screen)
        self.base_group.draw(self.screen)

        if DEBUG_MODE:
            self.render_debug(game_world)
            self.render_profile()

        pygame.display.flip()
        self.clock.tick()

    def render_debug(self, game_world):
        for row in range(self.grid_size[0]):
            for col in range(self.grid_size[1]):
                tile = game_world.map[row][col]
                text = self.font.render(f"({tile.row}, {tile.col})", True, (255, 255, 255))
                text_rect = text.get_rect(center=tile.rect.center)
                self.screen.blit(text, text_rect)

    def render_profile(self):
        # FPS Counter
        self.render_text(f"FPS: {int(self.clock.get_fps())}", (10, 10))

        # Memory usage
        self.render_text(f"Memory Usage: {process.memory_info().rss / 1024 / 1024:.2f} MB", (10, 30))

    def render_text(self, text, position):
        text_surface = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(text_surface, position)

    def quit(self):
        pygame.quit()
