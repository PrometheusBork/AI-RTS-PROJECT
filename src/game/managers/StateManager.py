import warnings

from src.game.interfaces.IObserveable import IObserveable
from src.game.constants.GameState import GameState
from src.game.interfaces.IObserver import IObserver


class GameStateManager(IObserveable, IObserver):
    def __init__(self):
        self._observers = set()
        self.state = GameState.MENU

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state
        self.notify(self.state)

    def toggle_pause(self):
        self.state = GameState.PAUSED if self.state == GameState.RUNNING else GameState.RUNNING
        self.notify(self.state)

    def update(self, new_state):
        if isinstance(new_state, GameState):
            self.set_state(new_state)
        else:
            warnings.warn(f"Invalid state {new_state} received by {self.__class__.__name__}")

    @property
    def observers(self):
        return self._observers

    def register(self, observer):
        self._observers.add(observer)

    def unregister(self, observer):
        self._observers.discard(observer)

    def notify(self, data=None):
        for observer in self._observers:
            observer.update(data)
