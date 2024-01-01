import numpy as np

from pytracer import Material
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytracer import HitRecord


class PointLightMaterial(Material):
    def __init__(self, emission: np.array):
        self.emission = emission

    def evaluate_brdf(self, hit_record: 'HitRecord', w_out: np.array, w_in: np.array) -> np.array:
        return np.array([0, 0, 0])

    def evaluate_emission(self, hit_record: 'HitRecord', w_out: np.array) -> np.array:
        return self.emission

    def has_specular_refraction(self) -> bool:
        return False

    def has_specular_reflexion(self) -> bool:
        return False

    def does_cast_shadows(self) -> bool:
        return False
