import random

# from pytracer import Scene
import numpy as np

from pytracer.ray import Ray


class DebugIntegrator:
    def __init__(self, scene):
        self.scene = scene

    def is_occluded(self, hit_position, light_dir, tolerance):
        shadow_ray = Ray(
            origin=np.copy(hit_position),
            direction=light_dir
        )
        shadow_hit = self.scene.intersectable_list.intersect(shadow_ray)

        if not shadow_hit.is_valid():
            return False

        dist_between_shadow_and_hit = np.copy(shadow_hit.position) - hit_position
        has_shadow_hit = shadow_hit.material.does_cast_shadows() and (
                dist_between_shadow_and_hit.dot(dist_between_shadow_and_hit) < tolerance)

        return has_shadow_hit

    def contribution_of(self, light_source, hit_record):
        light_hit = light_source.sample()
        light_direction = np.copy(light_hit.position) - hit_record.position
        d2 = light_direction.dot(light_direction)

        if self.is_occluded(hit_record.position, light_direction, d2):
            return np.array([0.0, 0.0, 0.0])

        brdf = hit_record.material.evaluate_brdf(hit_record, hit_record.w_in, light_direction)
        opposite_light_direction = -np.copy(light_direction)
        light_emission = light_hit.material.evaluate_emission(light_hit, opposite_light_direction)

        angle = 1.0
        if np.linalg.norm(light_hit.normal) > 0:
            angle = light_hit.normal.dot(light_direction)

        cos_theta_light = np.max([angle, 0])

        cos_theta = hit_record.normal.dot(light_direction)
        cos_theta = np.max([cos_theta, 0])

        # Multiply together factors relevant for shading, that is, brdf * light_emission * cos_theta_light * geometry term
        contribution = (1.0 / np.sqrt(d2)) * brdf * light_emission * cos_theta_light * cos_theta

        return contribution

    def integrate(self, ray: Ray):
        MAX_BOUNCES = 5

        hit_record = self.scene.intersectable_list.intersect(ray)

        if not hit_record.is_valid():
            return [0.0, 0.0, 0.0]

        emission = hit_record.material.evaluate_emission(hit_record, hit_record.w_in[:3])
        if emission is None:
            return emission

        reflection_contribution = np.array([0.0, 0.0, 0.0])
        refraction_contribution = np.array([0.0, 0.0, 0.0])

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

        contribution = np.array([0.0, 0.0, 0.0])
        for light_source in self.scene.light_sources:
            current_contribution = self.contribution_of(light_source, hit_record)
            contribution += current_contribution

        return contribution
