import pygame


class GameEngine:
    def __init__(self, game_world, game_render):
        self.game_world = game_world
        self.game_render = game_render
        self.movement_manager = game_render.movement_manager
        self.running = True
        self.clock = pygame.time.Clock()

    def run(self):
        while self.running:
            self.handle_events()
            self.render()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.handle_movement(None, "up")

    def handle_movement(self, unit, direction):
        self.movement_manager.move_object(unit, direction)

    def render(self):
        self.game_render.render()
