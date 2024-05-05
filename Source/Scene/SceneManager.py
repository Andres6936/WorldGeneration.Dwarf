from Source.Scene.IScene import IScene
from Source.Scene.SceneMain import SceneMain
from Source.Scene.TypeScene import TypeScene


class SceneManager:
    def __init__(self):
        self.running: bool = True
        self.mainScene: IScene = SceneMain()
        # Point to current scene to render
        self.currentScene: IScene = self.mainScene

    def isRunning(self):
        return self.running

    def events(self):
        typeScene: TypeScene = self.currentScene.events()
        if typeScene == TypeScene.NONE:
            pass
        elif typeScene == TypeScene.QUIT:
            self.running = False

    def clear(self):
        self.currentScene.clear()

    def draw(self):
        self.currentScene.draw()
