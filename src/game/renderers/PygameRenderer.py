import pygame
import psutil


class PygameRenderer:
    def __init__(self, screen_size, tile_size, hover_renderer):
        pygame.init()
        self.screen_size = screen_size
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("Game")
        self.hover_renderer = hover_renderer
        self.tile_size = tile_size
        self.font = pygame.font.SysFont('Arial', 14, bold=True)
        self.clock = pygame.time.Clock()
        self.process = psutil.Process()

    def render(self, sprite_groups):
        self.screen.fill((0, 0, 0))

        for sprite_group in sprite_groups.values():
            sprite_group.draw(self.screen)
            for sprite in sprite_group.sprites():
                if sprite.has_debug_info():
                    self.render_debug_info(sprite)

        self.hover_renderer.render_hover(pygame.mouse.get_pos(), self.screen)
        self.render_profile()

        pygame.display.flip()
        self.clock.tick()

    def render_debug_info(self, sprite):
        text = self.font.render(sprite.get_debug_info(), True, (255, 255, 255))
        text_rect = text.get_rect(center=sprite.rect.center)
        self.screen.blit(text, text_rect)

    def render_profile(self):
        # FPS Counter
        self.render_text(f"FPS: {int(self.clock.get_fps())}", (10, 10))

        # Memory usage
        self.render_text(f"Memory Usage: {self.process.memory_info().rss / 1024 / 1024:.1f} MB", (10, 25))

    def render_text(self, text, position):
        text_surface = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(text_surface, position)

    def quit(self):
        pygame.quit()
