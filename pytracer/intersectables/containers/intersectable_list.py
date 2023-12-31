from pytracer.hit_record import HitRecord
from pytracer.intersectables.intersectable import Intersectable
from pytracer.ray import Ray


class IntersectableList(Intersectable):
    def __init__(self):
        self.container = []

    def intersect(self, ray: Ray) -> HitRecord:
        """
        Implement ray-surface intersection in this method. Implementations of this
        method need to make and return a {@link HitRecord} correctly, following
        the conventions assumed for {@link HitRecord}.

        @param ray the ray used for intersection testing
        @return a hit record, should return an invalid hit record if there is no
          intersection
        """
        min_t = 10_000_000_000

        hit_record = HitRecord.make_empty()
        for intersectable in self.container:
            current_hit_record = intersectable.intersect(ray)
            if not current_hit_record.is_valid():
                continue

            current_t = current_hit_record.t
            if min_t > current_t > 0.0:
                min_t = current_t
                hit_record = HitRecord.make_from_other(current_hit_record)

        return hit_record

    def append(self, item: Intersectable):
        self.container.append(item)

    def at(self, index: int):
        return self.container[index]

    def size(self):
        return len(self.container)
