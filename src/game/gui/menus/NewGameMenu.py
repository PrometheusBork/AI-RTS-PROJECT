import pygame
import pygame_gui

from game.constants.GameState import GameState
from game.gui.components.Carousel import Carousel
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

        ## Add a carousel menu
        carousel_rect = pygame.Rect(0, 100, 300, 50)  # Adjust the size and position of the carousel
        carousel_rect.centerx = self.panel.rect.width / 2
        self.carousel = Carousel(
            relative_rect=carousel_rect,
            manager=self.gui_manager,
            container=self.panel,
            object_id='carousel'
        )

        # Add left arrow button
        left_arrow_rect = pygame.Rect(0, 0, 50, 50)
        left_arrow_rect.midleft = carousel_rect.midleft
        Button(
            relative_rect=left_arrow_rect,
            text="<",
            manager=self.gui_manager,
            container=self.panel,
            object_id='left_arrow_button',
            tool_tip_text='Previous map',
            on_click=self.scroll_left
        )

        # Add right arrow button
        right_arrow_rect = pygame.Rect(0, 0, 50, 50)
        right_arrow_rect.midright = carousel_rect.midright
        Button(
            relative_rect=right_arrow_rect,
            text=">",
            manager=self.gui_manager,
            container=self.panel,
            object_id='right_arrow_button',
            tool_tip_text='Next map',
            on_click=self.scroll_right
        )
        # Loop to add text labels to the carousel
        for i in range(1, 4):  # Adjust the range as needed
            item_rect = pygame.Rect(0, 0, 100, 50)  # Adjust the item size as needed
            item_rect.centerx = carousel_rect.width / 2 + (i - 1) * 100
            item = pygame_gui.elements.UILabel(
                relative_rect=item_rect,
                text=f"Map {i}",
                manager=self.gui_manager,
                container=self.carousel,  # Use the reference to the carousel object
                object_id=f'item_{i}'
            )
            self.carousel.add_item(item)  # Add the item to the carousel

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

    ## Add a scroll_left method
    def scroll_left(self):
        self.carousel.scroll(-1)

    ## Add a scroll_right method
    def scroll_right(self):
        self.carousel.scroll(1)

    ## Add a start method
    def start(self):
        self.menu_manager.state_manager.set_state(GameState.RUNNING)

    ## Add a back method
    def back(self):
        self.menu_manager.activate_menu("menu")

    ## Add an update method
    def update(self, delta_time):
        self.gui_manager.update(delta_time)

    ## Add a draw method
    def draw(self, surface):
        self.gui_manager.draw_ui(surface)

    ## Add a process_events method
    def process_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.gui_manager.process_events(event)

    ## Add a render method
    def render(self, surface):
        surface.fill((0, 0, 0))
        self.gui_manager.update(1)
        self.gui_manager.draw_ui(surface)
        pygame.display.update(self.panel_rect)

