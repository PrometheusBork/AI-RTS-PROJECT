import pygame

from game.constants.GameState import GameState
from game.managers.EventManager import EventManager
from game.constants.GlobalSettings import RESOURCE_TICK



class GameEngine:
    def __init__(self, game_world, game_render, state_manager):
        self.game_world = game_world
        self.game_render = game_render
        self.state_manager = state_manager
        state_manager.register(self.game_render)
        self.event_manager = EventManager(game_world, game_render, state_manager)
        self.clock = pygame.time.Clock()
        self.resource_time = 0
    
    def run(self):
        while self.state_manager.state != GameState.QUIT:
            self.render()
            self.clock.tick(60)
            if self.state_manager.state == GameState.RUNNING:
                if self.check_game_over() is True:
                    return("break")
                self.resource_time += RESOURCE_TICK
                if self.resource_time >= 4:
                    for player in self.event_manager.players:
                        player.add_resources(1)
                    self.resource_time = 0
            self.event_manager.handle_events()
        self.game_render.quit()

    def render(self):
        self.game_render.render()
