import numpy as np
from abc import ABC, abstractmethod

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytracer import HitRecord


class Material(ABC):
    """
    Materials implement functionality for shading surfaces using their BRDFs.
    Light sources are implemented using materials that return an emission term.
    """

    @abstractmethod
    def evaluate_brdf(self, hit_record: 'HitRecord', w_out: np.array, w_in: np.array) -> np.array:
        """
        Evaluate BRDF for pair of incoming and outgoing directions. This method
        is typically called by an integrator when the integrator obtained the
        incident direction by sampling a point on a light source.

        @param hit_record Information about hit point
        @param w_out Outgoing direction, normalized and pointing away from the
         surface
        @param w_in Incoming direction, normalized and pointing away from the
         surface
        @return BRDF value
        """

        pass

    @abstractmethod
    def evaluate_emission(self, hit_record: 'HitRecord', w_out: np.array) -> np.array:
        """
        Evaluate emission for outgoing direction. This method is typically
        called by an integrator when the integrator obtained the outgoing
        direction of the emission by sampling a point on a light source.

        @param hit_record Information about hit point on light source
        @param w_out Outgoing direction, normalized and pointing away from the
         surface
        @return emission value (vector with 3 elements)
        """

        pass

    @abstractmethod
    def has_specular_reflexion(self) -> bool:
        pass

    @abstractmethod
    def has_specular_refraction(self) -> bool:
        pass

    @abstractmethod
    def does_cast_shadows(self) -> bool:
        pass
