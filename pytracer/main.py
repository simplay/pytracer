from pytracer import Scene
from pytracer import Renderer

if __name__ == '__main__':
    scene_filepath = "../scenes/box1.json"
    scene = Scene(scene_filepath=scene_filepath, width=300, height=300)
    renderer = Renderer(scene)
    renderer.render(spp=1)
