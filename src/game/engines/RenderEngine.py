from game.managers.SpriteManager import SpriteManager
from game.renderers.HoverRenderer import HoverRenderer
from game.renderers.MenuRenderer import MenuRenderer
from game.renderers.PygameRenderer import PygameRenderer


class GameRender:
    def __init__(self, game_world, screen_size, tile_size):
        self.game_world = game_world
        self.screen_size = screen_size
        self.tile_size = tile_size

        # Sprite manager
        self.sprite_manager = SpriteManager()
        self.populate_sprite_groups()

        # Hover renderer
        self.hover_renderer = HoverRenderer()
        self.register_hoverable_objects()

        # Pygame renderer
        self.pygame_renderer = PygameRenderer(screen_size, tile_size, self.hover_renderer)

        # Menu renderer
        self.menu_renderer = MenuRenderer(screen_size)

    def populate_sprite_groups(self):
        for row in self.game_world.map:
            for tile in row:
                self.sprite_manager.add_sprite(tile)
                if not tile.is_empty():
                    self.sprite_manager.add_sprite(tile.game_object)

    def register_hoverable_objects(self):
        for row in self.game_world.map:
            for tile in row:
                self.hover_renderer.register_hoverable_object(tile)
                if not tile.is_empty():
                    self.hover_renderer.register_hoverable_object(tile.game_object)

    def render(self):
        self.menu_renderer.render(self.pygame_renderer.screen)
        # self.pygame_renderer.render(self.sprite_manager.sprite_groups)

    def quit(self):
        self.pygame_renderer.quit()
