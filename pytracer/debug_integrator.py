import random

from pytracer.ray import Ray


class DebugIntegrator:
    def integrate(self, ray: Ray):
        r, g, b = random.random(), 0.5, random.random()
        return [r, g, b]
