from interfaces.IHoverable import IHoverable
from interfaces.IMoveable import IMovable
from managers.MovementManager import MovementManager
from managers.SpriteManager import SpriteManager
from renderers.HoverRenderer import HoverRenderer
from renderers.PygameRenderer import PygameRenderer


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

        # Movement manager
        self.movement_manager = MovementManager(game_world)
        self.register_movable_objects()

        # Pygame renderer
        self.pygame_renderer = PygameRenderer(screen_size, tile_size, self.hover_renderer)

    def populate_sprite_groups(self):
        for row in self.game_world.map:
            for tile in row:
                self.sprite_manager.add_sprite(tile)
                if not tile.is_empty():
                    self.sprite_manager.add_sprite(tile.game_object)

    def register_hoverable_objects(self):
        for row in self.game_world.map:
            for tile in row:
                if isinstance(tile, IHoverable):
                    self.hover_renderer.register_hoverable_object(tile)
                if not tile.is_empty() and isinstance(tile.game_object, IHoverable):
                    self.hover_renderer.register_hoverable_object(tile.game_object)

    def register_movable_objects(self):
        for row in self.game_world.map:
            for tile in row:
                if not tile.is_empty() and isinstance(tile.game_object, IMovable):
                    self.movement_manager.register_movable_object(tile.game_object)

    def render(self):
        renderable_objects = []
        for row in self.game_world.map:
            for tile in row:
                renderable_objects.append(tile)
                if not tile.is_empty():
                    renderable_objects.append(tile.game_object)

        self.pygame_renderer.render(renderable_objects)

    def quit(self):
        self.pygame_renderer.quit()
