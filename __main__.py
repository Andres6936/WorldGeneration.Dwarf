from Source.Scene.SceneManager import SceneManager

if __name__ == '__main__':
    sceneManager = SceneManager()
    while sceneManager.isRunning():
        sceneManager.events()
        sceneManager.clear()
        sceneManager.draw()
