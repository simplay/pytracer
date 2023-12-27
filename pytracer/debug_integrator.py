import random

# from pytracer import Scene
import numpy as np

from pytracer.ray import Ray


def contribution_of(light_source, hit_record):
    light_hit = light_source.sample()
    light_direction = np.copy(light_hit.position) - hit_record.position
    d2 = light_direction.dot(light_direction)

    light_direction = light_direction / np.linalg.norm(light_direction)

    contribution = hit_record.material.evaluate_brdf(hit_record, hit_record.w_in, light_direction)
    light_emission = light_hit.material.evaluate_emission(light_hit, -light_direction)

    contribution = contribution * light_emission

    angle = hit_record.normal.dot(light_direction)
    cos_theta = 0.0 if 0.0 > angle else angle
    contribution *= cos_theta

    contribution *= (1.0 / d2)

    return contribution


class DebugIntegrator:
    def __init__(self, scene):
        self.scene = scene

    def integrate(self, ray: Ray):
        hit_record = self.scene.intersectable_list.intersect(ray)

        if not hit_record.is_valid():
            return [0, 0, 0]

        if hit_record.t > 0:

            # color = hit_record.intersectable.material.evaluate_brdf(None, None, None)

            contribution = np.array([0.0, 0.0, 0.0])
            for light_source in self.scene.light_sources:
                current_contribution = contribution_of(light_source, hit_record)
                contribution += current_contribution

            return contribution
            # return [0, 1, 0]

        # r, g, b = random.random(), 0.5, random.random()
        return [1, 0, 0]
