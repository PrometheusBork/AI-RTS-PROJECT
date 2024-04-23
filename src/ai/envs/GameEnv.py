import gym

from game.maps.Map import Map


class GameEnv(gym.Env):
    def __init__(self, game_engine, game_render):
        super(GameEnv, self).__init__()
        self.game_engine = game_engine
        self.render_engine = game_render

    def step(self, actions):
        self.game_engine.next_step(actions)
        self.render()

        observation = None
        rewards = 0.0  # Should return a list of rewards for each agent
        terminated = self.game_engine.check_game_over()
        truncated = False
        info = {}

        return observation, rewards, terminated, truncated, info

    def render(self):
        self.game_engine.render()

    def reset(self, seed=None, options=None):
        new_game = Map.select_map("map1")
        self.game_engine.reset(new_game)
        self.render()

    def close(self):
        self.game_engine.quit()
