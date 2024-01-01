from pytracer.light_sources.light_source import LightSource
from pytracer.hit_record import HitRecord
from pytracer.math.vec3 import Vec3


class PointLight(LightSource):
    def __init__(self, position: Vec3, emission: Vec3):
        from pytracer.materials.point_light_material import PointLightMaterial
        self.position = position
        self.emission = emission
        self.point_light_material = PointLightMaterial(emission)

    def sample(self) -> HitRecord:
        return HitRecord.make_with_material(Vec3.from_other(self.position), self.point_light_material)
