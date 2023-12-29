from pytracer import Camera
import numpy as np

from pytracer.debug_integrator import DebugIntegrator
from pytracer.diffuse import Diffuse
from pytracer.intersectable_list import IntersectableList
from pytracer.one_sampler import OneSampler
from pytracer.plane import Plane
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
        eye = np.array([0.01, 0.01, 5.0])
        look_at = np.array([0.01, 0.01, 0.01])
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
        r = 0.4
        sphere = Sphere(
            material=Diffuse(np.array([0, 0, 1])),
            center=np.array([0.0, 0.0, 0.0]),
            radius=r
        )
        self.intersectable_list.append(sphere)

        boring_gray = Diffuse((np.array([0.5, 0.5, 0.5])))
        distance = 3
        self.intersectable_list.append(Plane(boring_gray, normal=np.array([1.0, 0.0, 0.0]), distance=distance))
        self.intersectable_list.append(Plane(boring_gray, normal=np.array([-1.0, 0.0, 0.0]), distance=distance))
        self.intersectable_list.append(Plane(boring_gray, normal=np.array([0.0, 1.0, 0.0]), distance=distance))
        self.intersectable_list.append(Plane(boring_gray, normal=np.array([0.0, -1.0, 0.0]), distance=distance))
        self.intersectable_list.append(Plane(boring_gray, normal=np.array([0.0, 0.0, 1.0]), distance=distance))

    def build_light_sources(self):
        light_position = np.array([0.4, 0.6, 2.8])
        self.light_sources.append(
            PointLight(
                position=light_position,
                emission=10 * np.array([1, 1, 1])
            )
        )
        r = 0.03
        sphere = Sphere(
            material=Diffuse(np.array([1, 0, 0]), casts_shadows=False),
            center=light_position + 0.5*r*np.array([1, 1, 1]),
            radius=r
        )
        self.intersectable_list.append(sphere)

        light_position = np.array([0.4, 0.7, 0.4])
        self.light_sources.append(
            PointLight(
                position=light_position,
                emission=10 * np.array([0, 1, 1])
            )
        )
        r = 0.03
        sphere = Sphere(
            material=Diffuse(np.array([1, 0, 0]), casts_shadows=False),
            center=light_position + 0.5*r*np.array([1, 1, 1]),
            radius=r
        )
        self.intersectable_list.append(sphere)
