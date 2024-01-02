from pytracer.integrators.integrator import Integrator
from pytracer.math.vec3 import Vec3
from pytracer.ray import Ray

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytracer import HitRecord, Scene


class DebugIntegrator(Integrator):
    def __init__(self, scene: 'Scene'):
        self.scene = scene

    def integrate(self, ray: Ray) -> Vec3:
        hit_record = self.scene.intersectable_list.intersect(ray)
        if not hit_record.is_valid():
            return Vec3.zero()

        r, g, b = hit_record.normal[0], hit_record.normal[1], hit_record.normal[2]

        # color mapping to account for negative normal vector components
        nx = 0.5 * (r + 1.0)
        ny = 0.5 * (g + 1.0)
        nz = 0.5 * (b + 1.0)

        return Vec3(nx, ny, nz)
