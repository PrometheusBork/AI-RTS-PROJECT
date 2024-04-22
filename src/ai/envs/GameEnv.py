import gym

from game.maps.Map import Map


class GameEnv(gym.Env):
    def __init__(self, game_engine, game_render):
        super(GameEnv, self).__init__()
        self.game_engine = game_engine
        self.render_engine = game_render

    def step(self, action):
        self.game_engine.next_step(action)
        self.render()

        observation = None
        reward = 0.0
        terminated = self.game_engine.check_game_over()
        truncated = False
        info = {}

        return observation, reward, terminated, truncated, info

    def render(self):
        self.game_engine.render()

    def reset(self, seed=None, options=None):
        new_game = Map.select_map("map1")
        self.game_engine.reset(new_game)
        self.render()

    def close(self):
        self.game_engine.quit()
