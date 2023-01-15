from Source.Scene.IScene import IScene
from Source.Scene.SceneMain import SceneMain


class SceneManager:
    def __init__(self):
        self.running: bool = True
        self.mainScene: IScene = SceneMain()
        # Point to current scene to render
        self.currentScene: IScene = self.mainScene

    def isRunning(self):
        return self.running

    def events(self):
        self.currentScene.events()

    def clear(self):
        self.currentScene.clear()

    def draw(self):
        self.currentScene.draw()
