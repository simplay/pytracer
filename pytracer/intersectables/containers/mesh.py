from pytracer.intersectables.intersectable import Intersectable
from pytracer.ray import Ray


class Mesh(Intersectable):
    def intersect(self, ray: Ray) -> 'HitRecord':
        pass