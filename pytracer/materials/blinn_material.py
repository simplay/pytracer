import math

import numpy as np

from pytracer.material import Material


class BlinnMaterial(Material):
    """
    https://en.wikipedia.org/wiki/Blinn%E2%80%93Phong_reflection_model
    """

    def __init__(self, diffuse: 'np.array', specular: 'np.array', shininess: float):
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess

    def evaluate_brdf(self, hit_record: 'HitRecord', w_out: np.array, w_in: np.array) -> np.array:
        ambient_contribution = self.diffuse
        diffuse_contribution = self.diffuse * w_in.dot(hit_record.normal)

        half_vector = np.copy(w_in[:3]) + w_out[:3]
        half_vector = half_vector / np.linalg.norm(half_vector)
        specular_contribution = self.specular * math.pow(half_vector.dot(hit_record.normal), self.shininess)

        return ambient_contribution + diffuse_contribution + specular_contribution

    def evaluate_emission(self, hit_record: 'HitRecord', w_out: np.array) -> np.array:
        return np.array([0.0, 0.0, 0.0])

    def has_specular_reflexion(self) -> bool:
        return False

    def has_specular_refraction(self) -> bool:
        return False

    def does_cast_shadows(self) -> bool:
        return True
