from pytracer import Scene


class RenderTask:
    def __init__(self,
                 scene: Scene,
                 indices: list,
                 spp: int):

        self.width = scene.width
        self.height = scene.height
        self.indices = indices
        self.scene = scene
        self.spp = spp
