from pytracer import Scene
from pytracer import Renderer

if __name__ == '__main__':
    scene = Scene(width=640, height=480)
    renderer = Renderer(scene)
    renderer.render(spp=1)
