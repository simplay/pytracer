from pytracer import Scene
from pytracer import Renderer

if __name__ == '__main__':
    #scene = Scene(width=640, height=480)
    #scene = Scene(width=1000, height=1000)
    scene = Scene(width=1300, height=1300)
    renderer = Renderer(scene)
    renderer.render(spp=1)
