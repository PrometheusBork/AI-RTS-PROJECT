from game.abstracts.Observer import Observer
from game.managers.SpriteManager import SpriteManager
from game.renderers.HoverRenderer import HoverRenderer
from game.renderers.MenuRenderer import MenuRenderer
from game.renderers.PygameRenderer import PygameRenderer


class RenderEngine(Observer):
    def __init__(self, game_world, screen_size, tile_size, state_manager):
        self.game_world = game_world
        self.screen_size = screen_size
        self.tile_size = tile_size

        # Sprite manager
        self.sprite_manager = SpriteManager()
        self.populate_sprite_groups()

        # Hover renderer
        self.hover_renderer = HoverRenderer(game_world)
        self.hover_renderer.register_hoverable_objects()

        # Pygame renderer
        self.pygame_renderer = PygameRenderer(screen_size, tile_size, self.hover_renderer)

        # State manager
        self.state_manager = state_manager

        # Menu renderer
        self.menu_renderer = MenuRenderer(screen_size, state_manager)
        self.current_render_context = self.render_menu

    def populate_sprite_groups(self):
        for row in self.game_world.map:
            for tile in row:
                self.sprite_manager.add_sprite(tile)
                if not tile.is_empty():
                    self.sprite_manager.add_sprite(tile.game_object)

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
        elif new_state == current_state.QUIT:
            self.quit()

    def quit(self):
        self.pygame_renderer.quit()
