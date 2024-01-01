import numpy as np

from pytracer.hit_record import HitRecord
from pytracer.material import Material


class PointLightMaterial(Material):
    def __init__(self, emission: np.array):
        self.emission = emission

    def evaluate_brdf(self, hit_record: HitRecord, w_out: np.array, w_in: np.array) -> np.array:
        return np.array([0, 0, 0])

    def evaluate_emission(self, hit_record: HitRecord, w_out: np.array) -> np.array:
        return self.emission

    def has_specular_refraction(self) -> bool:
        return False

    def has_specular_reflexion(self) -> bool:
        return False

    def does_cast_shadows(self) -> bool:
        return False


class PointLight:
    def __init__(self, position: np.array, emission: np.array):
        self.position = position
        self.emission = emission
        self.point_light_material = PointLightMaterial(emission)

    def sample(self):
        return HitRecord.make_with_material(np.copy(self.position), self.point_light_material)
