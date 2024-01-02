import numpy as np

from pytracer.materials.material import Material
from pytracer.shading_sample import ShadingSample
from pytracer.math.vec3 import Vec3


class DiffuseMaterial(Material):
    def __init__(self, emission: Vec3, casts_shadows=True):
        """
        @param emission vector with rgb contributions
        @param casts_shadows, is True by default.
        """
        self.emission = emission / np.pi
        self.casts_shadows = casts_shadows

    def evaluate_brdf(self, hit_record: 'HitRecord', w_out: Vec3, w_in: Vec3) -> Vec3:
        return Vec3.from_other(self.emission)

    def evaluate_emission(self, hit_record: 'HitRecord', w_out: Vec3) -> Vec3:
        if hit_record.normal.dot(w_out) < 0:
            #hit_record.normal = -hit_record.normal
            pass

        return Vec3.zero()

    def has_specular_reflection(self) -> bool:
        return False

    def has_specular_refraction(self) -> bool:
        return False

    def does_cast_shadows(self) -> bool:
        return self.casts_shadows

    def evaluate_specular_reflection(self, hit_record: 'HitRecord') -> ShadingSample:
        return ShadingSample.make_empty()

    def evaluate_specular_refraction(self, hit_record: 'HitRecord') -> ShadingSample:
        return ShadingSample.make_empty()
