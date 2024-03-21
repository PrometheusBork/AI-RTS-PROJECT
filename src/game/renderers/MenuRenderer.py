import pygame_gui
import pygame

from game.gui.components.Button import Button


class MenuRenderer:
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.gui_manager = pygame_gui.UIManager(screen_size, 'src/game/gui/style/style.json', enable_live_theme_updates=True)
        self.panel_rect = pygame.Rect(0, 0, 300, 300)
        self.panel_rect.center = (self.screen_size[0] / 2, self.screen_size[1] / 2)
        self.panel = pygame_gui.elements.UIPanel(
            relative_rect=self.panel_rect,
            starting_height=1,
            manager=self.gui_manager,
        )
        self.setup_menu()

    def setup_menu(self):
        print("Setting up menu")
        button_rect = pygame.Rect(0, 50, 200, 50)
        button_rect.centerx = self.panel_rect.width / 2
        Button(rect=button_rect, text="Start Game", manager=self.gui_manager, container=self.panel, on_click=self.start_game)

    def start_game(self):
        print("Game started")

    def render(self, surface):
        self.gui_manager.update(1)
        self.gui_manager.draw_ui(surface)
        pygame.display.update()
