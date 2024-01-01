from abc import ABC, abstractmethod

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytracer import HitRecord


class LightSource(ABC):
    @abstractmethod
    def sample(self) -> 'HitRecord':
        pass
