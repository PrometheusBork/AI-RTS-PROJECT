import random

import gym

from game.constants.GameState import GameState
from src.game.maps.Map import Map
from src.game.engines.RenderEngine import RenderEngine
from src.game.managers.StateManager import GameStateManager
from src.game.engines.GameEngine import GameEngine


class GameEnv(gym.Env):
    def __init__(self):
        self._grid_size = (10, 10)
        self._tile_size = 50
        self._screen_size = (self._grid_size[0] * self._tile_size + (2 * self._tile_size) + 200,
                             self._grid_size[1] * self._tile_size + (2 * self._tile_size))

        self.game_world = Map.select_map("map1")
        self.state_manager = GameStateManager()
        self.state_manager.set_state(GameState.RUNNING)
        self.render_engine = RenderEngine(self.game_world, self._screen_size, self._tile_size, self.state_manager,
                                          skip_menu=True)
        self.game_engine = GameEngine(self.game_world, self.render_engine, self.state_manager)

        self.steps_per_action = 30
        self.current_step = 0

        while True:
            self.step(5)

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


if __name__ == "__main__":
    env = GameEnv()
