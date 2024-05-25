from abc import ABC, abstractmethod


class IObserveable(ABC):
    @property
    @abstractmethod
    def observers(self) -> set:
        """
        Get the set of observers.
        """

    @abstractmethod
    def register(self, observer) -> None:
        """
        Register an observer to this the list of observers.
        """

    @abstractmethod
    def unregister(self, observer) -> None:
        """
        Unregister an observer from the list of observers.
        """

    @abstractmethod
    def notify(self, data=None) -> None:
        """
        Notify all observers of a change in the observeable object.
        """
