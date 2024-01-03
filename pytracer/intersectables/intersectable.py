from abc import ABC, abstractmethod

from pytracer.ray import Ray

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytracer import HitRecord


class Intersectable(ABC):

    @abstractmethod
    def intersect(self, ray: Ray) -> 'HitRecord':
        """
        Implement ray-surface intersection in this method. Implementations of this
        method need to make and return a {@link HitRecord} correctly, following
        the conventions assumed for {@link HitRecord}.

        @param ray the ray used for intersection testing
        @return a hit record, should return an invalid hit record if there is no intersection
        """

        pass
