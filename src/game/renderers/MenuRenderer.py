import pygame_gui
import pygame

class MenuRenderer:
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.gui_manager = pygame_gui.UIManager(screen_size)
        self.setup_menu()

    def setup_menu(self):
        print("Setting up menu")

        button_rect = pygame.Rect(0, 50, 400, 50)
        button_rect.centerx = self.screen_size[0] / 2
        self.new_game_button = pygame_gui.elements.UIButton(
            relative_rect=button_rect,
            text="New game",
            manager=self.gui_manager,
            container=pygame_gui.elements.UIPanel(
                relative_rect=pygame.Rect(0, 0, 600, 300),
                starting_height=1,
                manager=self.gui_manager
            ),
            object_id='new_game_button',
            tool_tip_text='Start a new game',
        )

        button_rect = pygame.Rect(0, 110, 400, 50)
        button_rect.centerx = self.screen_size[0] / 2
        self.options_button = pygame_gui.elements.UIButton(
            relative_rect=button_rect,
            text="Options",
            manager=self.gui_manager,
            container=pygame_gui.elements.UIPanel(
                relative_rect=pygame.Rect(0, 0, 600, 300),
                starting_height=1,
                manager=self.gui_manager
            ),
            object_id='options_button',
            tool_tip_text='Go to options',
        )

        button_rect = pygame.Rect(0, 170, 400, 50)
        button_rect.centerx = self.screen_size[0] / 2
        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=button_rect,
            text="Exit",
            manager=self.gui_manager,
            container=pygame_gui.elements.UIPanel(
                relative_rect=pygame.Rect(0, 0, 600, 300),
                starting_height=1,
                manager=self.gui_manager
            ),
            object_id='exit_button',
            tool_tip_text='Exit the game',
        )

    def render(self, surface):
        self.gui_manager.update(1)
        self.gui_manager.draw_ui(surface)
        pygame.display.update()

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.new_game_button:
                    print("Game started")
                elif event.ui_element == self.options_button:
                    print("Options game")
                elif event.ui_element == self.exit_button:
                    print("Exit game")
        self.gui_manager.process_events(event)
        return True

# Initialization
pygame.init()
screen_size = (800, 600)
surface = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Menu')

menu_renderer = MenuRenderer(screen_size)

# Main loop
running = True
while running:
    surface.fill((92,96,77))
    for event in pygame.event.get():
        if not menu_renderer.handle_events(event):
            running = False
    menu_renderer.render(surface)

pygame.quit()
