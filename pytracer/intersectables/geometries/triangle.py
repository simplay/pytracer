import numpy as np

from pytracer.hit_record import HitRecord
from pytracer.intersectables.intersectable import Intersectable
from pytracer.ray import Ray

from typing import TYPE_CHECKING

from pytracer.math.vec3 import Vec3

if TYPE_CHECKING:
    from pytracer import Material


class Triangle(Intersectable):
    """
    Construct a plane given its normal and distance to the origin Note that the
    distance is along the direction that the normal points (meaning that the
    sign of distance matters)
    """

    def __init__(self, material: 'Material', a: Vec3, b: Vec3, c: Vec3, face_id: int):
        self.material = material
        self.a = a
        self.b = b
        self.c = c
        self.face_id = face_id

    def compute_normal(self, _alpha: float = 0.0, _beta: float = 0.0):
        ba = self.b - self.a
        ca = self.c - self.a
        return ba.cross(ca).normalized()

    def intersect(self, ray: Ray) -> HitRecord:
        """
        A triangle T can be spanned by a set of three points A, B, and C, i.e., T = span(A, B, C)
        Every point P within such a triangle T fulfills P = w * A + u * B + v * C with the conditions
        0 <= u, v, w <= 1 AND u + v + w = 1 (Eq. 1)

        Normalized representation of such triangle points is given as follows:
        P = A + u*(B-A) + v(C-A) (Eq. 2)
        <=>
        P = (1 - u - v) * A + u * B + v * C (which corresponds to Eq. 1 for w = 1 - u - v)

        The ray-triangle intersection can be computed using the following identities:

        Ray P = O + t * D with O := origin and D := direction
        Triangle P = A + u * (B - A) + v * (C - A)

        Formulate system of equations for P_ray = P_triangle
        <=>
        O + t * D = A + u * (B - A) + v * (C - A)
        <=>
        O - A = u * (B - A) + v * (C - A) - t * D
        <=>

        [O - A] = [B - A | C - A | -D] * [u, v, t]'
        <=>
        y = M * x, here M and y are known
        => solve for x = inv(M) * y

        the resulting x = [u, v, t]' gives us the barycentric coordinates of
        the point P in the triangle. We can the perform an intersection test by
        verifying the initial conditions (1) 0 <= u, v <= 1 and (2) u + v + w = 1

        @param ray
        """
        ba = self.b - self.a
        ca = self.c - self.a
        oa = ray.origin - self.a
        d = -ray.direction

        M = np.array([
            [ba[0], ca[0], d[0]],
            [ba[1], ca[1], d[1]],
            [ba[2], ca[2], d[2]]
        ])

        u, v, t = np.linalg.inv(M).dot(oa)

        if u < 0.0 or u > 1.0:
            return HitRecord.make_empty()

        if v < 0.0 or v > 1.0:
            return HitRecord.make_empty()

        # u + v + w = 1
        sum = u + v
        if sum > 1.0 or sum < 0.0:
            return HitRecord.make_empty()

        intersection_position = ray.point_at(t)
        hit_normal = self.compute_normal(0, 0)
        w_in = ray.direction.incident_direction()
        hit_tangent = Vec3.one()  # TODO: fixme

        hit_record = HitRecord(
            t=t,
            position=intersection_position,
            normal=hit_normal,
            w_in=w_in,
            tangent=hit_tangent,
            intersectable=self,
            material=self.material
        )
        return hit_record


class MeshTriangle(Triangle):
    def __init__(self, material: 'Material', a: Vec3, b: Vec3, c: Vec3, nx: Vec3, ny: Vec3, nz: Vec3, face_id: int):
        super().__init__(material, a, b, c, face_id)
        self.nx = nx
        self.ny = ny
        self.nz = nz

    def compute_normal(self, u: float, v: float):
        w = 1 - u - v
        normal = Vec3.from_other(w * self.nx + u * self.ny + v * self.nz)
        normal.normalized()
        return normal
