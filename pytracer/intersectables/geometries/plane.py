import numpy as np

from pytracer.hit_record import HitRecord
from pytracer.intersectables.intersectable import Intersectable
from pytracer.ray import Ray

from typing import TYPE_CHECKING

from pytracer.math.vec3 import Vec3

if TYPE_CHECKING:
    from pytracer import Material


class Plane(Intersectable):

    # A*x + B*y + C*z + D = 0
    def __init__(self, material: 'Material', normal: Vec3, distance: float):
        self.material = material
        self.distance = distance
        self.normal = normal

    def intersect(self, ray: Ray) -> HitRecord:
        """
        @param ray
        @return HitRecord

        In the following a derivation of the intersection formula we are using in this implementation to compute the plane ray intersection:

        A plane can be defined by a normal n and a point p0 on the plane. In this case, every other point p on the plane fulfills:
        dot(p - p0, n) = 0

        This identity is the implicit representation of a plane.

        A point on a ray is given by the parameterization r(t) = o + t*d where
            o := (ox, oy, oz) denotes tzhe origion of the ray and
            d := (dx, dy, dz)= denotes the direction of the ray and
            t denotes a float-valued parameter

            By setting p = r(t) and using the plane definition, we get:
            dot(r(t) - p0, n) = dot(o + t*d - p0, n) = 0

            <=>

            dot(t*d, n) + dot(o-p0, n) = 0

            because dot(t*d, n) t * dot(d, n)

            and thus
            t = -dot(o-p0, n) / dot(d, n)
              = dot(p0-0, n) / dot(d, n)

            which is the definition of the intersection parameter t.

            However, we can further simplify the formula of t when assuming that the normal is always pointing outwards, i.e., pointing away from the origin.
            In combination with the fact that p0 is defined ass p0 = m * (o- n), where m denotes a scalar. Notice that (o-n) is an inwards pointing normal (the normal that points towards the viewer)

            This is useful when we want to define a plane by a distance value m and a normal n: By using this assumption, we can simplify the expression

            dot(p0 - o, n) = dot(m * (o-n) - o, n)
            = m * dot(-n, n) - dot(o, n)
            = m * (-1) * dot(n, n) - dot(o, n)
            = m * (-1) * 1 - dot(o, n)
            = -m - dot(o, n)
            = -(m + dot(o, n))

            and hence derive

            t = - (m + dot(o, n)) / dot(d, n)

        """
        # angle theta between the ray direction and the plane normal
        # cos_theta = ray.direction[:3].dot(self.normal)
        cos_theta = self.normal.dot(ray.direction)

        # TODO: handle to small normals and return an empty hit
        if np.abs(cos_theta) <= 0.000001:
            return HitRecord.make_empty()

        # assumption: point is zero and then we shift by distance
        t = -(self.distance + ray.origin.dot(self.normal)) / cos_theta

        if t <= 0:
            return HitRecord.make_empty()

        intersection_position = ray.point_at(t)
        w_in = ray.direction.incident_direction()

        hit_normal = Vec3(*self.normal)
        hit_tangent = Vec3.one().cross(hit_normal)

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
