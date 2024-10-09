import pygame

from src.game.constants.GameState import GameState
from src.game.managers.EventManager import EventManager
from src.game.constants.GlobalSettings import RESOURCE_TICK


class GameEngine:
    def __init__(self, game_world, game_render, state_manager):
        self.game_world = game_world
        self.game_render = game_render
        self.game_render.menu_renderer.register(state_manager)
        self.state_manager = state_manager
        state_manager.register(game_render)
        self.event_manager = EventManager(game_world, game_render, state_manager)
        self.clock = pygame.time.Clock()
        self.resource_time = 0
        self.agents = None

    def run(self):
        while self.state_manager.state != GameState.QUIT:
            self.next_step()
            self.render()
            return "break"
        self.quit()

    def next_step(self, actions=None):
        self.event_manager.handle_events()

        if self.state_manager.state == GameState.RUNNING:
            self.event_manager.handle_ai(actions)
            self.resource_time += RESOURCE_TICK
            self.update_resources()
        self.clock.tick(60)

    def update_resources(self):
        self.resource_time += RESOURCE_TICK
        if self.resource_time >= 4:
            for player in self.game_world.player_manager.players:
                player.add_resources(10)
            self.resource_time = 0

    def setup_agents(self):
        self.event_manager = EventManager(self.game_world, self.game_render, self.state_manager)

    def check_game_over(self):
        return any(player.base.is_destroyed() for player in self.game_world.player_manager.players)

    def reset(self, game_world):
        self.game_world = game_world
        self.state_manager.set_state(GameState.RUNNING)
        self.event_manager.reset(game_world)
        self.game_render.reset(game_world)
        self.resource_time = 0

    def render(self):
        self.game_render.render()

    def quit(self):
        self.game_render.quit()
