from abc import ABC, abstractmethod


class IScene(ABC):
    @abstractmethod
    def events(self):
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def clear(self):
        pass
