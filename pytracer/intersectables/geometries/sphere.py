import numpy as np

from pytracer.hit_record import HitRecord
from pytracer.intersectables.intersectable import Intersectable
from pytracer.materials.material import Material
from pytracer.ray import Ray


class Sphere(Intersectable):
    def __init__(self,
                 material: Material,
                 center: np.array,
                 radius: float):

        """
        @param material
        @param center
        @param radius
        """

        self.material = material
        self.center = center
        self.radius = radius

    def intersect(self, ray: Ray) -> HitRecord:
        """
        Details how to compute the ray-sphere intersection:

        A point on ray is given by the parametrization
        r(t) = o + t*d [1] where
        o := (ox, oy, oz) denotes the origin of the ray and
        d := (dx, dy, dz) denotes the direction of the ray and
        t is float-valued parameter

        the implicit formulation of the surface of a sphere is given by
        (x-x0)^2 + (y - y0)^2 + (z - z0)^2 = r^2
        <=>
        ||P-C||^2 = r^2 [2] where
        P := (x, y, z) a point on the sphere
        C := (x0, y0, z0) denotes the center of the sphere

        Notice [1] can further be reformulated to
        dot(P-C, P-C) = r^2 [3]

        There is an intersection IFF a point on a ray is on the surface on the sphere,
        i.e. intersection IFF P = R(t). [4]
        With the definitions of [1] and [3] and the fact [4] we can derive
        ((ox - t*dx) - x0)^2 + ((oy - t*dy) - y0)^2 + ((oz - t*dz) - z0)^2 = r^2
        by expanding and rearranging we finally get:
        t^2 * dot(d, d) + 2*t*dot(d, o - C) + dot(o - c, o - c) - r^2 = 0 [5]
        This is a quadratic equation of the form a*t^2 + b*t + c = 0 [6] where
        a := dot(d, d), b := 2 * dot(d, o - C) and c := dot(o - c, o - c) - r^2

        The solutions of an equation of the form [5] is given by
        t = -b +- sqrt(b^2 - 4*a*c) / (2*a) where
        b^2 - 4*a*c denotes the discriminant of the equation

        If discriminant < 0 j, the line of the ray does not intersect the sphere (missed);
        If discriminant = 0 the line of the ray just touches the sphere in one point (tangent);
        If discriminant > 0, the line of the ray touches the sphere in two points (intersected).

        There are 3 different ways to intersect a sphere:

        1. There is no intersection
        2. There is one intersection point (i.e. the ray is a tangent on the plane)
        3. There are two intersection points (ray penetrates the sphere):
         a) if both t are positive, the ray is facing the sphere and intersecting
         b) if one t is positive and one negative, the ray is shooting from inside
         c) if both t are negative, the ray is shooting away from the sphere

        For computing the hitRecord of the intersection, we are interested in the
        smaller and positive t.
        """

        oc = np.copy(ray.origin[:3]) - self.center
        rd = np.copy(ray.direction[:3])

        a = rd.dot(rd)
        b = 2.0 * rd.dot(oc)
        c = oc.dot(oc) - self.radius ** 2.0

        discriminant = b * b - 4.0 * a * c

        zeros = []
        if discriminant >= 0.0:
            t1 = (-b + np.sqrt(discriminant)) / (2.0 * a)
            t2 = (-b - np.sqrt(discriminant)) / (2.0 * a)
            zeros = [t1, t2]

        if len(zeros) < 2:
            return HitRecord.make_empty()
        else:
            t = np.min(zeros)
            if t < 0:
                t = np.max(zeros)
                if t < 0:
                    return HitRecord.make_empty()

        hit_position = ray.point_at(t)
        hit_normal = (1.0 / self.radius) * (np.copy(hit_position) - self.center)

        w_in = -np.copy(ray.direction)
        w_in = w_in / np.linalg.norm(w_in)

        hit_record = HitRecord(
            t=t,
            position=hit_position,
            normal=hit_normal,
            tangent=np.array([0, 0, 0]),
            w_in=w_in,
            material=self.material,
            intersectable=self,
            i=ray.i,
            j=ray.j
        )

        return hit_record
