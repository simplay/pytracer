from pytracer.math.vec3 import Vec3


class ShadingSample:
    def __init__(self, brdf: Vec3, emission: Vec3, w: Vec3, is_specular: bool, p: float, is_valid=True):
        self.brdf = brdf
        self.emission = emission
        self.w = w
        self.is_specular = is_specular
        self.p = p
        self.is_valid = is_valid

    @classmethod
    def make_empty(cls):
        return ShadingSample(
            brdf=Vec3.zero(),
            emission=Vec3.zero(),
            w=Vec3.zero(),
            is_specular=False,
            p=0,
            is_valid=False
        )
