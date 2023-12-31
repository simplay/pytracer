import numpy as np


class ShadingSample:
    def __init__(self, brdf: np.array, emission: np.array, w: np.array, is_specular: bool, p: float, is_valid=True):
        self.brdf = brdf
        self.emission = emission
        self.w = w
        self.is_specular = is_specular
        self.p = p
        self.is_valid = is_valid

    @classmethod
    def make_empty(cls):
        return ShadingSample(
            brdf=np.array([0.0, 0.0, 0.0]),
            emission=np.array([0.0, 0.0, 0.0]),
            w=np.array([0.0, 0.0, 0.0]),
            is_specular=False,
            p=0,
            is_valid=False
        )
