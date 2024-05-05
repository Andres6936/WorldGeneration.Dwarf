from abc import ABC, abstractmethod

from Source.Scene.TypeScene import TypeScene


class IScene(ABC):
    @abstractmethod
    def events(self) -> TypeScene:
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def clear(self):
        pass
