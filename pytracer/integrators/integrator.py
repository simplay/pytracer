from abc import ABC, abstractmethod

import numpy as np

from pytracer.ray import Ray


class Integrator(ABC):
    @abstractmethod
    def integrate(self, ray: Ray) -> np.array:
        pass
