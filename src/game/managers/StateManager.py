from game.constants.GameState import GameState


class GameStateManager:
    def __init__(self):
        self.state = GameState.RUNNING

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def toggle_pause(self):
        self.state = GameState.PAUSED if self.state == GameState.RUNNING else GameState.RUNNING
