import numpy as np

from pytracer.material import Material
from pytracer.shading_sample import ShadingSample


class Reflective(Material):
    def __init__(self, ks: np.array):
        self.ks = ks

    def evaluate_brdf(self, hit_record, w_out, w_in) -> np.array:
        return np.array([1.0, 1.0, 1.0])

    def evaluate_emission(self, hit_record, w_out) -> np.array:
        return np.array([0.0, 0.0, 0.0])

    def has_specular_reflexion(self) -> bool:
        return True

    def has_specular_refraction(self) -> bool:
        return False

    def does_cast_shadows(self) -> bool:
        return True

    @staticmethod
    def inv_reflected(w_in, normal):
        cos_theta_i = normal.dot(w_in)
        return 2.0 * cos_theta_i * normal - w_in

    def evaluate_specular_reflection(self, hit_record):
        reflected_direction = Reflective.inv_reflected(hit_record.w_in[:3], hit_record.normal)
        return ShadingSample(
            brdf=self.ks,
            emission=np.array([0.0, 0.0, 0.0]),
            w=reflected_direction,
            is_specular=True,
            p=1
        )
