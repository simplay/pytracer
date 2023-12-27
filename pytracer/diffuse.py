import numpy as np

from pytracer.material import Material


class Diffuse(Material):
    def __init__(self, emission: np.array):
        """
        @param [np.array] vector with rgb contributions
        """
        self.emission = emission * (1.0 / np.pi)

    def evaluate_brdf(self, hit_record, w_out, w_in) -> np.array:
        return self.emission

    def evaluate_emission(self, _hit_record, _w_out) -> np.array:
        return np.array([0, 0, 0])

    def has_specular_reflexion(self) -> bool:
        return False

    def has_specular_refraction(self) -> bool:
        return False

    def does_cast_shadows(self) -> bool:
        return True
