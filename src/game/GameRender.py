import pygame
import psutil

from game.objects.Tree import Tree
from game.objects.Base import Base
from game.tiles.GrassTile import GrassTile
from game.tiles.WaterTile import WaterTile

DEBUG_MODE = True
process = psutil.Process()


class GameRender:
    def __init__(self, screen_size, grid_size, tile_size):
        pygame.init()
        self.screen_size = screen_size
        self.grid_size = grid_size
        self.tile_size = tile_size

        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("Game")

        self.font = pygame.font.SysFont('Arial', 12)
        self.clock = pygame.time.Clock()

    def render(self, game_world):
        self.screen.fill((0, 0, 0))
        self.render_grid(game_world)
        self.render_profile()

        pygame.display.flip()
        self.clock.tick()

    def render_grid(self, game_world):
        for row in range(self.grid_size[0]):
            for col in range(self.grid_size[1]):
                tile = game_world.map[row][col]
                tile_rect = pygame.Rect(col * self.tile_size + self.tile_size, row * self.tile_size + self.tile_size,
                                        self.tile_size - 1, self.tile_size - 1)
                self.render_tile(tile, tile_rect)

                # Render game objects on the tile
                for game_object in tile.game_objects:
                    self.render_game_object(game_object)

    def render_tile(self, tile, tile_rect):
        if isinstance(tile, GrassTile):
            pygame.draw.rect(self.screen, (0, 130, 44), tile_rect)
        elif isinstance(tile, WaterTile):
            pygame.draw.rect(self.screen, (7, 6, 130), tile_rect)
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), tile_rect, 1)

        if DEBUG_MODE:
            text = self.font.render(f"({tile.row}, {tile.col})", True, (255, 255, 255))
            text_rect = text.get_rect(center=tile_rect.center)
            self.screen.blit(text, text_rect)

    def render_profile(self):
        # FPS Counter
        self.render_text(f"FPS: {int(self.clock.get_fps())}", (10, 10))

        # Memory usage
        self.render_text(f"Memory Usage: {process.memory_info().rss / 1024 / 1024:.2f} MB", (10, 30))

    def render_text(self, text, position):
        text_surface = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(text_surface, position)

    def render_game_object(self, game_object):
        if isinstance(game_object, Tree):
            game_object.render(self)
        if isinstance(game_object, Base):
            game_object.render(self)

    def quit(self):
        pygame.quit()
