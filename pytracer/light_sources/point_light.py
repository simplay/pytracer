import numpy as np

from pytracer.light_sources.light_source import LightSource
from pytracer.hit_record import HitRecord


class PointLight(LightSource):
    def __init__(self, position: np.array, emission: np.array):
        from pytracer.materials.point_light_material import PointLightMaterial
        self.position = position
        self.emission = emission
        self.point_light_material = PointLightMaterial(emission)

    def sample(self) -> HitRecord:
        return HitRecord.make_with_material(np.copy(self.position), self.point_light_material)
