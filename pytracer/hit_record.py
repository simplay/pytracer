from pytracer.intersectables.intersectable import Intersectable
from pytracer.materials.material import Material
from pytracer.math.vec3 import Vec3


class HitRecord:
    def __init__(self,
                 t: float,
                 position: Vec3,
                 normal: Vec3,
                 tangent: Vec3,
                 w_in: Vec3,
                 material: Material,
                 intersectable: Intersectable,
                 i=0,  # TODO: rename to u
                 j=0,  # j TODO: rename to v texture lookup coordinates in plane space
                 is_null=False):
        """
        @param t parameter on ray where the hit occurred.
        @param position where the ray hit the surface
        @param normal normal-vector on the surface where the ray was intersecting
        @param tangent tangent-vector on the surface where the ray was intersecting
        @param w_in incident direction towards origin of ray that hit surface.
            By convention, it points away from the surface, that is, in the direction opposite to the incident ray.
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
        self.is_null = is_null

    @classmethod
    def make_empty(cls):
        hit_record = HitRecord(
            t=0,
            position=Vec3.zero(),
            normal=Vec3.zero(),
            tangent=Vec3.zero(),
            w_in=Vec3.zero(),
            material=None,
            intersectable=None,
            i=0,
            j=0,
            is_null=True
        )
        return hit_record

    @classmethod
    def make_with_material(cls, position: Vec3, material: Material) -> 'HitRecord':
        hit_record = HitRecord(
            t=0.0,
            position=position,
            normal=Vec3.zero(),
            tangent=Vec3.zero(),
            w_in=Vec3.zero(),
            material=material,
            intersectable=None,
            i=-1,
            j=-1,
            is_null=False
        )
        return hit_record

    @classmethod
    def make_from_other(cls, other_hit_record: 'HitRecord') -> 'HitRecord':
        hit_record = HitRecord(
            t=other_hit_record.t,
            position=Vec3.from_other(other_hit_record.position),
            normal=Vec3.from_other(other_hit_record.normal),
            tangent=Vec3.from_other(other_hit_record.tangent),
            w_in=Vec3.from_other(other_hit_record.w_in),
            material=other_hit_record.material,
            intersectable=other_hit_record.intersectable,
            i=other_hit_record.i,
            j=other_hit_record.j,
            is_null=other_hit_record.is_null
        )
        return hit_record

    def is_valid(self) -> bool:
        return not self.is_null
