import numpy as np

from pytracer.intersectable import Intersectable
from pytracer.material import Material


class HitRecord:
    def __int__(self,
                t: float,
                position: np.array,
                normal: np.array,
                tangent: np.array,
                w_in: np.array,
                material: Material,
                intersectable: Intersectable,
                i=0,
                j=0):
        """
        @param t parameter on ray where the hit occurred.
        @param normal normal-vector on the surface where the ray was intersecting
        @param tangent tangent-vector on the surface where the ray was intersecting
        @param w_in incident direction
        @param material surface property
        @param intersectable the object that was hit
        @param i [int]
        @param j [int]
        """

        self.t = t
        self.position = position
        self.normal = normal
        self.tangent = tangent
        self.w_in = w_in
        self.material = material
        self.intersectable = intersectable
        self.i = i
        self.j = j

    @classmethod
    def make_empty(cls, position, material):
        return HitRecord(
            t=0,
            position=position,
            normal=np.array([0, 0, 0]),
            tangent=np.array([0, 0, 0]),
            w_in=np.array([0, 0, 0]),
            material=material,
            i=0,
            j=0
        )

    def transform(self, matrix: np.array):
        return None
