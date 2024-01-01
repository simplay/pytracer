from pytracer.math.vec3 import Vec3


class Ray:
    ESP = 0.00001

    def __init__(self, origin: Vec3, direction: Vec3, i=-1, j=-1, perturbate=True, bounces=0):
        """
        @param origin
        @param direction
        @param i
        @param j
        @param perturbate [bool] if true the ray is slightly perurbated to enhance the overall sampling quality and thus reduce the variance in the rendered image.
        """

        self.origin = origin
        self.direction = direction
        self.i = i
        self.j = j
        self.perturbate = perturbate
        self.bounces = bounces

        if perturbate:
            self.origin = Ray.ESP * direction + origin

    def point_at(self, t: float):
        return t * self.direction + self.origin
