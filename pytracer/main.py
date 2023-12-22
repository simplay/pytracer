from pytracer import Scene
from pytracer import Renderer

counter = None


def init(args):
    """ store counter for later use """
    global counter
    counter = args


def process(index: int):
    global counter

    # TODO: do not increment anything here
    # with counter.get_lock():
    #     counter.value += 1

    # print(counter.value)

    return index ** 2


if __name__ == '__main__':
    scene = Scene(width=640, height=480)
    renderer = Renderer(scene)
    renderer.render(3, 3)
