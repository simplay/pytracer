import numpy as np

from typing import TYPE_CHECKING

from pytracer.integrators.integrator import Integrator
from pytracer.ray import Ray
from pytracer.math.vec3 import Vec3

if TYPE_CHECKING:
    from pytracer import HitRecord, Scene


class WhittedIntegrator(Integrator):
    """
    http://gec.di.uminho.pt/DISCIP/Minf/IFR0708/TP/pbrtTutorial3.pdf
    """

    def __init__(self, scene: 'Scene'):
        self.scene = scene

    def is_occluded(self, hit_position: Vec3, light_dir: Vec3, tolerance: float) -> bool:
        shadow_ray = Ray(
            origin=Vec3.from_other(hit_position),
            direction=light_dir
        )
        shadow_hit = self.scene.intersectable_list.intersect(shadow_ray)

        if not shadow_hit.is_valid():
            return False

        dist_between_shadow_and_hit = shadow_hit.position - hit_position
        has_shadow_hit = shadow_hit.material.does_cast_shadows() and (
                dist_between_shadow_and_hit.dot(dist_between_shadow_and_hit) < tolerance)

        return has_shadow_hit

    def contribution_of(self, light_source: Vec3, hit_record: 'HitRecord') -> Vec3:
        light_hit = light_source.sample()
        light_direction = light_hit.position - hit_record.position
        d2 = light_direction.dot(light_direction)

        if self.is_occluded(hit_record.position, light_direction, d2):
            return Vec3.zero()

        brdf = hit_record.material.evaluate_brdf(hit_record, hit_record.w_in, light_direction)
        light_emission = light_hit.material.evaluate_emission(light_hit, -light_direction)

        angle = 1.0
        if np.linalg.norm(light_hit.normal) > 0:
            angle = light_hit.normal.dot(light_direction)

        cos_theta_light = np.max([angle, 0])

        cos_theta = hit_record.normal.dot(light_direction)
        cos_theta = np.max([cos_theta, 0])

        # Multiply together factors relevant for shading, that is, brdf * light_emission * cos_theta_light * geometry term
        contribution = (1.0 / np.sqrt(d2)) * brdf * light_emission * cos_theta_light * cos_theta

        return contribution

    def integrate(self, ray: Ray) -> Vec3:
        MAX_BOUNCES = 5

        hit_record = self.scene.intersectable_list.intersect(ray)

        if not hit_record.is_valid():
            return Vec3.zero()

        emission = hit_record.material.evaluate_emission(hit_record, hit_record.w_in[:3])
        if emission is None:
            return emission

        reflection_contribution = Vec3.zero()
        refraction_contribution = Vec3.zero()

        if hit_record.material.has_specular_reflexion() and ray.bounces < MAX_BOUNCES:
            sample = hit_record.material.evaluate_specular_reflection(hit_record)
            if sample.is_valid:
                reflection_contribution = np.copy(sample.brdf)
                reflected_ray = Ray(
                    origin=np.copy(hit_record.position),
                    direction=sample.w,
                    bounces=ray.bounces + 1
                )
                spec = self.integrate(reflected_ray)
                reflection_contribution *= spec

        if hit_record.material.has_specular_reflexion() or hit_record.material.has_specular_refraction():
            return reflection_contribution + refraction_contribution

        contribution = Vec3.zero()
        for light_source in self.scene.light_sources:
            current_contribution = self.contribution_of(light_source, hit_record)
            contribution += current_contribution

        return contribution
