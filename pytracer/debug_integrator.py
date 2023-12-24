import random

#from pytracer import Scene
from pytracer.ray import Ray


class DebugIntegrator:
    def __init__(self, scene):
        self.scene = scene

    def integrate(self, ray: Ray):
        hit_record = self.scene.intersectable_list.intersect(ray)
        if not hit_record.is_valid():
            return [0, 0, 0]

        if hit_record.t > 0:
            return [0, 1, 0]

        # r, g, b = random.random(), 0.5, random.random()
        return [1, 0, 0]
