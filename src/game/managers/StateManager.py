from game.interfaces.IObserveable import IObserveable
from game.constants.GameState import GameState


class GameStateManager(IObserveable):
    def __init__(self):
        self._observers = []
        self.state = GameState.MENU

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state
        self.notify(self.state)

    def toggle_pause(self):
        self.state = GameState.PAUSED if self.state == GameState.RUNNING else GameState.RUNNING
        self.notify(self.state)

    @property
    def observers(self) -> list:
        return self._observers

    def register(self, observer) -> None:
        self._observers.append(observer)

    def unregister(self, observer) -> None:
        self._observers.remove(observer)

    def notify(self, data=None) -> None:
        for observer in self._observers:
            observer.update(data)
