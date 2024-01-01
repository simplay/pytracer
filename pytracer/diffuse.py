import numpy as np

from pytracer.material import Material


class Diffuse(Material):
    def __init__(self, emission: np.array, casts_shadows=True):
        """
        @param [np.array] vector with rgb contributions
        """
        self.emission = emission / np.pi
        self.casts_shadows = casts_shadows

    def evaluate_brdf(self, hit_record: 'HitRecord', w_out: np.array, w_in: np.array) -> np.array:
        return self.emission

    def evaluate_emission(self, hit_record: 'HitRecord', w_out: np.array) -> np.array:
        if hit_record.normal.dot(w_out) < 0:
            hit_record.normal = -hit_record.normal

        return np.array([0, 0, 0])

    def has_specular_reflexion(self) -> bool:
        return False

    def has_specular_refraction(self) -> bool:
        return False

    def does_cast_shadows(self) -> bool:
        return self.casts_shadows
