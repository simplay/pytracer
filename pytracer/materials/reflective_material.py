from pytracer.materials.material import Material
from pytracer.shading_sample import ShadingSample
from pytracer.math.vec3 import Vec3


class ReflectiveMaterial(Material):
    def __init__(self, ks: Vec3):
        self.ks = ks

    def evaluate_brdf(self, hit_record: 'HitRecord', w_out: Vec3, w_in: Vec3) -> Vec3:
        return Vec3.one()

    def evaluate_emission(self, hit_record: 'HitRecord', w_out: Vec3) -> Vec3:
        return Vec3.zero()

    def has_specular_reflexion(self) -> bool:
        return True

    def has_specular_refraction(self) -> bool:
        return False

    def does_cast_shadows(self) -> bool:
        return True

    def evaluate_specular_reflection(self, hit_record: 'HitRecord') -> ShadingSample:
        reflected_direction: Vec3 = hit_record.w_in.reflected_on(hit_record.normal)
        return ShadingSample(
            brdf=self.ks,
            emission=Vec3.zero(),
            w=reflected_direction,
            is_specular=True,
            p=1.0
        )
