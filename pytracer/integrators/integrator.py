from abc import ABC, abstractmethod

from pytracer.ray import Ray
from pytracer.math.vec3 import Vec3


class Integrator(ABC):
    @abstractmethod
    def integrate(self, ray: Ray) -> Vec3:
        pass
