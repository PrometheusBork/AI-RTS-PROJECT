import pygame
import pygame_gui


class OptionMenu:
    def __init__(self, screen_size, menu_manager):
        self.screen_size = screen_size
        self.menu_manager = menu_manager
        self.gui_manager = pygame_gui.UIManager(screen_size, 'src/game/gui/style/style.json', enable_live_theme_updates=True)
        self.panel_rect = pygame.Rect(0, 0, 300, 300)
        self.panel_rect.center = (self.screen_size[0] / 2, self.screen_size[1] / 2)
        self.panel = pygame_gui.elements.UIPanel(
            relative_rect=self.panel_rect,
            starting_height=1,
            manager=self.gui_manager,
        )

    def process_events(self, events):
        pass
        # Process events for the options menu UI elements

    def render(self, surface):
        surface.fill((0, 0, 0))
        self.gui_manager.update(1)
        self.gui_manager.draw_ui(surface)
        pygame.display.update(self.panel_rect)
