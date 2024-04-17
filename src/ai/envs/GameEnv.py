import random

import gym

from game.maps.Map import Map

class GameEnv(gym.Env):
    def __init__(self, game_world, game_render, game_engine, state_manager, grid_size, tile_size, screen_size):
        self._grid_size = grid_size
        self._tile_size = tile_size
        self._screen_size = screen_size

        self.game_world = game_world
        self.state_manager = state_manager
        self.render_engine = game_render
        self.game_engine = game_engine

        self.steps_per_action = 30
        self.current_step = 0

        while True:
            self.step(5)
            if self.game_engine.check_game_over() is True:
                break

    def step(self, action):
        observation = None
        reward = 0.0
        done = False
        info = {}

        self.current_step += 1

        #if self.current_step % self.steps_per_action == 0:
        self.game_engine.next_step(random.randint(1, 6))
        #else:
        #    self.game_engine.next_step(None)

        self.render()

        return observation, reward, done, info

    def render(self):
        self.game_engine.render()

    def reset(self):
        new_game = Map.select_map("map1")
        self.game_engine.reset()
        self.game_engine.game_world = new_game
        self.render_engine.game_world = new_game

    def close(self):
        self.game_engine.quit()