import math

from pytracer.materials.material import Material
from pytracer.shading_sample import ShadingSample
from pytracer.math.vec3 import Vec3


class BlinnMaterial(Material):
    """
    https://en.wikipedia.org/wiki/Blinn%E2%80%93Phong_reflection_model
    """

    def __init__(self, diffuse: Vec3, specular: Vec3, shininess: float):
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess

    def evaluate_brdf(self, hit_record: 'HitRecord', w_out: Vec3, w_in: Vec3) -> Vec3:
        ambient_contribution = self.diffuse
        diffuse_contribution = self.diffuse * w_in.dot(hit_record.normal)

        half_vector = Vec3.from_other(w_in + w_out).normalized()
        specular_contribution = self.specular * math.pow(half_vector.dot(hit_record.normal), self.shininess)

        return ambient_contribution + diffuse_contribution + specular_contribution

    def evaluate_emission(self, hit_record: 'HitRecord', w_out: Vec3) -> Vec3:
        return Vec3.zero()

    def has_specular_reflexion(self) -> bool:
        return False

    def has_specular_refraction(self) -> bool:
        return False

    def does_cast_shadows(self) -> bool:
        return True

    def evaluate_specular_reflection(self, hit_record: 'HitRecord') -> ShadingSample:
        return ShadingSample.make_empty()
