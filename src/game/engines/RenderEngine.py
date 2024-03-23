from game.managers.SpriteManager import SpriteManager
from game.renderers.HoverRenderer import HoverRenderer
from game.renderers.PygameRenderer import PygameRenderer


class GameRender:
    def __init__(self, game_world, screen_size, tile_size):
        self.game_world = game_world
        self.screen_size = screen_size
        self.tile_size = tile_size

        # Sprite manager
        self.sprite_manager = SpriteManager(game_world)
        self.sprite_manager.register_sprite_groups()

        # Hover renderer
        self.hover_renderer = HoverRenderer(game_world)
        self.hover_renderer.register_hoverable_objects()

        # Pygame renderer
        self.pygame_renderer = PygameRenderer(screen_size, tile_size, self.hover_renderer)

    def render(self):
        self.pygame_renderer.render(self.sprite_manager.sprite_groups)

    def quit(self):
        self.pygame_renderer.quit()
