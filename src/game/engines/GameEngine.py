import pygame

from game.constants.GameState import GameState
from game.managers.MovementManager import MovementManager
from game.constants.GlobalSettings import RESOURCE_TICK



class GameEngine:
    def __init__(self, game_world, game_render, state_manager):
        self.game_world = game_world
        self.game_render = game_render
        self.state_manager = state_manager
        self.state_manager.register(self.game_render)
        self.movement_manager = MovementManager(game_world)
        self.clock = pygame.time.Clock()
        self.resource_time = 0
        self.players = game_world.player_manager.players
    
    def run(self):
        self.movement_manager.register_movable_objects()
        while self.state_manager.state != GameState.QUIT:
            self.render()
            self.clock.tick(60)
            self.resource_time += RESOURCE_TICK
            if self.resource_time >= 4:
                for player in self.players:
                    player.add_resources(1)
                self.resource_time = 0
            self.handle_events()
        self.game_render.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state_manager.set_state(GameState.QUIT)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.handle_movement("up")
                if event.key == pygame.K_DOWN:
                    self.handle_movement("down")
                if event.key == pygame.K_LEFT:
                    self.handle_movement("left")
                if event.key == pygame.K_RIGHT:
                    self.handle_movement("right")
                if event.key == pygame.K_ESCAPE:
                    self.state_manager.set_state(GameState.QUIT)
                if event.key == pygame.K_p:
                    self.state_manager.toggle_pause()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.game_render.menu_renderer.gui_manager.process_events(event)

    def handle_movement(self, direction):
        if self.state_manager.state == GameState.RUNNING:
            self.movement_manager.move_objects(direction)

    def render(self):
        self.game_render.render()
