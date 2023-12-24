import numpy as np


class Ray:
    ESP = 0.00001

    def __init__(self, origin: np.array, direction: np.array, i=-1, j=-1, perturbate=False):
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

        if perturbate:
            self.origin = Ray.ESP * direction + origin

    def point_at(self, t: float):
        hit_position = t * np.copy(self.direction[:3]) + self.origin
        return hit_position
