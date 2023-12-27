from pytracer import Camera
import numpy as np

from pytracer.debug_integrator import DebugIntegrator
from pytracer.diffuse import Diffuse
from pytracer.intersectable_list import IntersectableList
from pytracer.one_sampler import OneSampler
from pytracer.point_light import PointLight
from pytracer.sphere import Sphere


class Scene:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.camera = self.build_camera()
        self.sampler = OneSampler()
        self.integrator = DebugIntegrator(self)
        self.intersectable_list = IntersectableList()
        self.light_sources = []

        self.build_intersectables()
        self.build_light_sources()

    def build_camera(self):
        eye = np.array([0.0, 0.0, 3.0])
        look_at = np.array([0.0, 0.0, 0.0])
        up = np.array([0.0, 1.0, 0.0])
        aspect_ratio = self.width / self.height
        return Camera(eye=eye,
                      look_at=look_at,
                      up=up,
                      fov=60.0,
                      aspect_ratio=aspect_ratio,
                      width=self.width,
                      height=self.height)

    def build_intersectables(self):
        r = 1.5
        sphere = Sphere(
            material=Diffuse(np.array([0, 0, 1])),
            center=np.array([-r, -r, 0.0]),
            radius=r
        )
        self.intersectable_list.append(sphere)

    def build_light_sources(self):
        self.light_sources.append(
            PointLight(
                position=np.array([0.5, 0.5, 2.0]),
                emission=10*np.array([1, 1, 1])
            )
        )
