import pygame

from game.constants.GameState import GameState
from game.managers.EventManager import EventManager
from game.constants.GlobalSettings import RESOURCE_TICK



class GameEngine:
    def __init__(self, game_world, game_render, state_manager):
        self.game_world = game_world
        self.game_render = game_render
        self.state_manager = state_manager
        state_manager.register(game_render)
        self.event_manager = EventManager(game_world, game_render, state_manager)
        self.clock = pygame.time.Clock()
        self.resource_time = 0
        self.event_manager.selection_manager.register_selectable_objects()
        self.event_manager.movement_manager.register_movable_objects()
    
    def run(self):
        while self.state_manager.state != GameState.QUIT:
            self.next_step(None)
            self.render()
            return "break"
        self.quit()

    def next_step(self, action):
        self.event_manager.handle_events()
        if self.state_manager.state == GameState.RUNNING:
            self.event_manager.handle_ai(action)
            self.resource_time += RESOURCE_TICK
            if self.resource_time >= 4:
                for player in self.game_world.player_manager.players:
                    player.add_resources(10)
                print("Resources:", [player.resources for player in self.game_world.player_manager.players])
                self.resource_time = 0
        self.clock.tick(60)

    def check_game_over(self):
        for player in self.game_world.player_manager.players:
            if player.base.is_destroyed():
                print(f"Player {player} has lost the game!")
                return True
        return False

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
