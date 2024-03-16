import pygame
import psutil

from game.objects.Tree import Tree
from game.objects.Base import Base
from game.units.Unit import Unit
from game.tiles.Tile import Tile

DEBUG_MODE = True
process = psutil.Process()


class GameRender:
    def __init__(self, game_world, screen_size, tile_size):
        pygame.init()
        self.screen_size = screen_size
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("Game")
        self.grid_size = (len(game_world.map), len(game_world.map[0]))
        self.tile_size = tile_size
        self.font = pygame.font.SysFont('Arial', 12, bold=True)
        self.clock = pygame.time.Clock()

        self.sprite_group = {
            Tile: pygame.sprite.Group(),
            Base: pygame.sprite.Group(),
            Tree: pygame.sprite.Group(),
            Unit: pygame.sprite.Group(),
        }

        self.populate_group_map(game_world)

    def populate_group_map(self, game_world):
        for row in game_world.map:
            for tile in row:
                self.sprite_group[Tile].add(tile)
                if not tile.is_empty():
                    self.categorize_objects(tile)

    def categorize_objects(self, tile):
        if isinstance(tile.game_object, Tree):
            self.sprite_group[Tree].add(tile.game_object)
        elif isinstance(tile.game_object, Base):
            self.sprite_group[Base].add(tile.game_object)
        elif isinstance(tile.game_object, Unit):
            self.sprite_group[Unit].add(tile.game_object)

    def render(self, game_world):
        self.screen.fill((0, 0, 0))
        self.sprite_group[Tile].draw(self.screen)
        self.sprite_group[Tree].draw(self.screen)
        self.sprite_group[Base].draw(self.screen)
        self.sprite_group[Unit].draw(self.screen)

        if DEBUG_MODE:
            self.render_debug(game_world)
            self.render_profile()

        pygame.display.flip()
        self.clock.tick()

    def render_debug(self, game_world):
        for row in range(self.grid_size[0]):
            for col in range(self.grid_size[1]):
                tile = game_world.map[row][col]
                text = self.font.render(f"({tile.position[0]}, {tile.position[1]})", True, (255, 255, 255))
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
