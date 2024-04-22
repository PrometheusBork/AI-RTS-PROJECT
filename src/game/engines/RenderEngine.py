from game.interfaces.IObserver import IObserver
from game.managers.SpriteManager import SpriteManager
from game.renderers.HoverRenderer import HoverRenderer
from game.renderers.MenuRenderer import MenuRenderer
from game.renderers.PygameRenderer import PygameRenderer


class RenderEngine(IObserver):
    def __init__(self, game_world, screen_size, tile_size, state_manager, skip_menu=False):
        self.game_world = game_world
        self.screen_size = screen_size
        self.tile_size = tile_size

        self.sprite_manager = SpriteManager(game_world)
        self.hover_renderer = HoverRenderer(game_world)
        self.pygame_renderer = PygameRenderer(screen_size, tile_size, self.hover_renderer)

        # State manager
        self.state_manager = state_manager

        # Menu renderer
        self.menu_renderer = MenuRenderer(screen_size, state_manager)
        if skip_menu:
            self.current_render_context = self.render_game
        else:
            self.current_render_context = self.render_menu

    def render(self):
        self.current_render_context()

    def render_game(self):
        self.pygame_renderer.render(self.sprite_manager.sprite_groups)

    def render_menu(self):
        self.menu_renderer.render(self.pygame_renderer.screen)

    def update(self, new_state):
        current_state = self.state_manager.get_state()
        if new_state == current_state.RUNNING:
            self.current_render_context = self.render_game
        elif new_state == current_state.MENU:
            self.current_render_context = self.render_menu
        elif new_state == current_state.QUIT:
            self.quit()

    def reset(self, game_world):
        self.game_world = game_world
        self.sprite_manager.reset(game_world)
        self.hover_renderer.reset(game_world)

    def quit(self):
        self.pygame_renderer.quit()
