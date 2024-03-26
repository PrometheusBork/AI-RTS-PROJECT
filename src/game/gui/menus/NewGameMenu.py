import pygame
import pygame_gui

from game.constants.GameState import GameState
from game.gui.components.Button import Button

class NewGameMenu:
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

        self.title = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(0, 0, 300, 50),
            text='New game',
            manager=self.gui_manager,
            container=self.panel,
        )

        self.setup_menu()

    def setup_menu(self):

        button_rect = pygame.Rect(0, 50, 200, 50)
        button_rect.centerx = self.panel.rect.width / 2
        Button(
            relative_rect=button_rect,
            text="Start",
            manager=self.gui_manager,
            container=self.panel,
            object_id='start_button',
            tool_tip_text='Start a new game',
            on_click=self.start
        )

        button_rect = pygame.Rect(0, 170, 200, 50)
        button_rect.centerx = self.panel.rect.width / 2
        Button(
            relative_rect=button_rect,
            text="Back",
            manager=self.gui_manager,
            container=self.panel,
            object_id='back_button',
            tool_tip_text='Go back to main menu',
            on_click=self.back
        )
    
    def start(self):
        self.menu_manager.state_manager.set_state(GameState.RUNNING)

    def back(self):
        self.menu_manager.activate_menu("menu")

    def process_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.gui_manager.process_events(event)

    def render(self, surface):
        surface.fill((0, 0, 0))
        self.gui_manager.update(1)
        self.gui_manager.draw_ui(surface)
        pygame.display.update(self.panel_rect)
