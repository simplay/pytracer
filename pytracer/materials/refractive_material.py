import math

from pytracer.materials.material import Material
import numpy as np

from pytracer.math.vec3 import Vec3
from pytracer.shading_sample import ShadingSample


class RefractiveMaterial(Material):
    def __init__(self, refraction_index: float, ks: Vec3):
        self.refraction_index = refraction_index
        self.ks = ks

    """
    https://blog.demofox.org/2017/01/09/raytracing-reflection-refraction-fresnel-total-internal-reflection-and-beers-law/
    https://en.wikipedia.org/wiki/Snell%27s_law
    """

    def fresnel_factor(self, hit_record: 'HitRecord') -> float:
        w_in = -Vec3.from_other(hit_record.w_in).normalized()
        normal = Vec3.from_other(hit_record.normal)

        # enters material
        n1 = 1.0
        n2 = self.refraction_index

        # leaves material
        if hit_record.normal.dot(hit_record.w_in) <= 0.0:
            n1 = self.refraction_index
            n2 = 1.0
            normal = -normal

        cos_theta_i = -w_in.dot(normal)
        phase_velocity = n1 / n2
        sin_sq_theta_t = math.pow(phase_velocity, 2.0) * (1.0 - pow(cos_theta_i, 2.0))

        if sin_sq_theta_t > 1.0:
            return 1.0

        r0 = ((n1 - n2) / (n1 + n2)) ** 2.0

        if n1 <= n2:
            x = 1.0 - cos_theta_i
            return r0 + (1.0 - r0) * math.pow(x, 5.0)

        cos_theta_t = np.sqrt(1.0 - sin_sq_theta_t)
        x = 1.0 - cos_theta_t
        return r0 + (1.0 - r0) * math.pow(x, 5.0)

    def evaluate_brdf(self, hit_record: 'HitRecord', w_out: Vec3, w_in: Vec3) -> Vec3:
        return Vec3.zero()

    def evaluate_emission(self, hit_record: 'HitRecord', w_out: Vec3) -> Vec3:
        return Vec3.zero()

    def has_specular_reflection(self) -> bool:
        return True

    def has_specular_refraction(self) -> bool:
        return True

    def does_cast_shadows(self) -> bool:
        return False

    def evaluate_specular_reflection(self, hit_record: 'HitRecord') -> ShadingSample:
        reflected_direction = hit_record.w_in.reflected_on(hit_record.normal)
        r = self.fresnel_factor(hit_record)
        return ShadingSample(
            brdf=Vec3(r, r, r),
            emission=Vec3.zero(),
            w=reflected_direction,
            is_specular=True,
            p=r
        )

    def evaluate_specular_refraction(self, hit_record: 'HitRecord') -> ShadingSample:
        w_in = -Vec3.from_other(hit_record.w_in).normalized()
        normal = Vec3.from_other(hit_record.normal)

        # enters material
        n1 = 1.0
        n2 = self.refraction_index

        # leaves material
        if hit_record.normal.dot(hit_record.w_in) <= 0.0:
            n1 = self.refraction_index
            n2 = 1.0
            normal = -normal

        cos_theta_i = -w_in.dot(normal)
        phase_velocity = n1 / n2
        sin_sq_theta_t = math.pow(phase_velocity, 2.0) * (1.0 - pow(cos_theta_i, 2.0))

        if sin_sq_theta_t > 1.0:
            return ShadingSample.make_empty()

        refracted_direction = phase_velocity * w_in

        scaled_normal = (phase_velocity * cos_theta_i - np.sqrt(1.0 - sin_sq_theta_t)) * normal
        refracted_direction = refracted_direction + scaled_normal

        r = self.fresnel_factor(hit_record)
        brdf = (1.0 - r) * self.ks

        return ShadingSample(
            brdf=brdf,
            emission=Vec3.zero(),
            w=refracted_direction,
            is_specular=True,
            p=r
        )
