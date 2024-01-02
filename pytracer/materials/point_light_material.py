from pytracer import Material
from typing import TYPE_CHECKING

from pytracer.shading_sample import ShadingSample
from pytracer.math.vec3 import Vec3

if TYPE_CHECKING:
    from pytracer import HitRecord


class PointLightMaterial(Material):
    def __init__(self, emission: Vec3):
        self.emission = emission

    def evaluate_brdf(self, hit_record: 'HitRecord', w_out: Vec3, w_in: Vec3) -> Vec3:
        return Vec3.zero()

    def evaluate_emission(self, hit_record: 'HitRecord', w_out: Vec3) -> Vec3:
        return self.emission

    def has_specular_refraction(self) -> bool:
        return False

    def has_specular_reflection(self) -> bool:
        return False

    def does_cast_shadows(self) -> bool:
        return False

    def evaluate_specular_reflection(self, hit_record: 'HitRecord') -> ShadingSample:
        return ShadingSample.make_empty()

    def evaluate_specular_refraction(self, hit_record: 'HitRecord') -> ShadingSample:
        return ShadingSample.make_empty()
