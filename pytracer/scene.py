from pytracer import Camera
import numpy as np

from pytracer.debug_integrator import DebugIntegrator
from pytracer.one_sampler import OneSampler


class Scene:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.camera = self.build_camera()
        self.sampler = OneSampler()
        self.integrator = DebugIntegrator()

    def build_camera(self):
        eye = np.array([0.5, 0.5, 0.5])
        look_at = np.array([0.5, 0.0, 0.0])
        up = np.array([0.0, 1.0, 0.0])
        aspect_ratio = self.width / self.height
        return Camera(eye=eye,
                      look_at=look_at,
                      up=up,
                      fov=60.0,
                      aspect_ratio=aspect_ratio,
                      width=self.width,
                      height=self.height)
