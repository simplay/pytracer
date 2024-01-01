import numpy as np


class Vec3(np.ndarray):
    def __new__(cls, *args):
        x, y, z, *_ = args
        return np.asarray([x, y, z]).view(cls)

    @classmethod
    def from_other(cls, other: np.ndarray) -> 'Vec3':
        return Vec3(*other)

    @classmethod
    def zero(cls) -> 'Vec3':
        return Vec3(0.0, 0.0, 0.0)

    @classmethod
    def one(cls) -> 'Vec3':
        return Vec3(1.0, 1.0, 1.0)

    def dotted(self) -> float:
        return self.dot(self)

    def reflected_on(self, normal: 'Vec3') -> 'Vec':
        cos_theta_i = normal.dot(self)
        return 2.0 * cos_theta_i * normal - self

    def incident_direction(self) -> 'Vec3':
        return -Vec3(*self).normalized()

    def cross(self, other: 'Vec3') -> 'Vec3':
        return Vec3(*np.cross(self, other))

    def normalized(self) -> 'Vec3':
        return Vec3(*self / np.linalg.norm(self))
