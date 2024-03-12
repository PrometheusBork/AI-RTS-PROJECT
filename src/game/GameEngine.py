import pygame


class GameEngine:
    def __init__(self, game_world, game_render):
        self.game_world = game_world
        self.game_render = game_render
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

    def render(self):
        self.game_render.render(self.game_world)
