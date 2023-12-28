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

        light_direction = light_direction / np.linalg.norm(light_direction)

        if self.is_occluded(hit_record.position, light_direction, d2):
            return np.array([0.0, 0.0, 0.0])

        contribution = hit_record.material.evaluate_brdf(hit_record, hit_record.w_in, light_direction)
        opposite_light_direction = -np.copy(light_hit.position)
        light_emission = light_hit.material.evaluate_emission(light_hit, opposite_light_direction)

        contribution = contribution * light_emission

        angle = hit_record.normal.dot(light_direction)
        cos_theta = np.max([angle, 0])
        contribution *= cos_theta

        contribution /= d2

        return contribution

    def integrate(self, ray: Ray):
        hit_record = self.scene.intersectable_list.intersect(ray)

        if not hit_record.is_valid():
            return [0.0, 0.0, 0.0]

        if hit_record.t > 0.0:
            # return [0, 1, 0]

            # color = hit_record.intersectable.material.evaluate_brdf(None, None, None)

            contribution = np.array([0.0, 0.0, 0.0])
            for light_source in self.scene.light_sources:
                current_contribution = self.contribution_of(light_source, hit_record)
                contribution += current_contribution

            return contribution

        # r, g, b = random.random(), 0.5, random.random()
        return [1, 0, 0]
