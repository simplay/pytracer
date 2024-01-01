import numpy as np

from pytracer.material import Material
from pytracer.shading_sample import ShadingSample


class ReflectiveMaterial(Material):
    def __init__(self, ks: np.array):
        self.ks = ks

    def evaluate_brdf(self, hit_record: 'HitRecord', w_out: np.array, w_in: np.array) -> np.array:
        return np.array([1.0, 1.0, 1.0])

    def evaluate_emission(self, hit_record: 'HitRecord', w_out: np.array) -> np.array:
        return np.array([0.0, 0.0, 0.0])

    def has_specular_reflexion(self) -> bool:
        return True

    def has_specular_refraction(self) -> bool:
        return False

    def does_cast_shadows(self) -> bool:
        return True

    # TODO: move to material
    @staticmethod
    def inv_reflected(w_in: np.array, normal: np.array):
        cos_theta_i = normal.dot(w_in)
        return 2.0 * cos_theta_i * normal - w_in

    # TODO: move to material
    def evaluate_specular_reflection(self, hit_record: 'HitRecord'):
        reflected_direction = ReflectiveMaterial.inv_reflected(hit_record.w_in[:3], hit_record.normal)
        return ShadingSample(
            brdf=self.ks,
            emission=np.array([0.0, 0.0, 0.0]),
            w=reflected_direction,
            is_specular=True,
            p=1
        )
