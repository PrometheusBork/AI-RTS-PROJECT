import pygame_gui
import pygame

from src.game.constants.GameState import GameState
from src.game.gui.components.Button import Button
from src.game.interfaces.IObserveable import IObserveable


class MenuRenderer(IObserveable):
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self._observers = set()
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
        button_rect = pygame.Rect(0, 50, 200, 50)
        button_rect.centerx = self.panel.rect.width / 2
        Button(
            relative_rect=button_rect,
            text="New game",
            manager=self.gui_manager,
            container=self.panel,
            object_id='new_game_button',
            tool_tip_text='Start a new game',
            on_click=self.new_game
        )

        button_rect = pygame.Rect(0, 110, 200, 50)
        button_rect.centerx = self.panel.rect.width / 2
        Button(
            relative_rect=button_rect,
            text="Options",
            manager=self.gui_manager,
            container=self.panel,
            object_id='options_button',
            tool_tip_text='Go to options',
            on_click=None
        ).disable()

        button_rect = pygame.Rect(0, 170, 200, 50)
        button_rect.centerx = self.panel.rect.width / 2
        Button(
            relative_rect=button_rect,
            text="Exit",
            manager=self.gui_manager,
            container=self.panel,
            object_id='exit_button',
            tool_tip_text='Exit the game',
            on_click=self.exit_game
        )

    def new_game(self):
        self.notify(GameState.RUNNING)

    def exit_game(self):
        self.notify(GameState.QUIT)

    @property
    def observers(self):
        return self._observers

    def register(self, observer):
        self._observers.add(observer)

    def unregister(self, observer):
        self._observers.discard(observer)

    def notify(self, data=None):
        for observer in self._observers:
            observer.update(data)

    def render(self, surface):
        surface.fill((0, 0, 0))
        self.gui_manager.update(1)
        self.gui_manager.draw_ui(surface)
        pygame.display.update(self.panel_rect)  # Only update the panel rect
