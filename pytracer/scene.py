import json

from pytracer import Camera

from pytracer.materials.blinn_material import BlinnMaterial
from pytracer.integrators.whitted_integrator import WhittedIntegrator
from pytracer.materials.diffuse_material import DiffuseMaterial
from pytracer.intersectables.containers.intersectable_list import IntersectableList
from pytracer.one_sampler import OneSampler
from pytracer.intersectables.geometries.plane import Plane
from pytracer.light_sources.point_light import PointLight
from pytracer.materials.reflective_material import ReflectiveMaterial
from pytracer.intersectables.geometries.sphere import Sphere
from pytracer.math.vec3 import Vec3


class Scene:
    MATERIALS = {
        "blinn": lambda params: BlinnMaterial(diffuse=Vec3(*params["diffuse"]),
                                              specular=Vec3(*params["specular"]),
                                              shininess=params["shininess"]),
        "reflective": lambda params: ReflectiveMaterial(ks=Vec3(*params["ks"])),
        "diffuse": lambda params: DiffuseMaterial(emission=Vec3(*params["emission"]))
    }

    LIGHT_TYPES = {
        "point_light": lambda params: PointLight(position=Vec3(*params["position"]),
                                                 emission=Vec3(*params["emission"]))
    }

    INTEGRATORS = {
        "whitted": WhittedIntegrator
    }

    def __init__(self, scene_filepath: str, width: int, height: int):
        with open(scene_filepath) as file:
            scene_description = json.load(file)

        self.width = width
        self.height = height

        self.camera = self.build_camera(camera_params=scene_description["camera"])
        self.sampler = OneSampler()
        self.integrator = self.INTEGRATORS[scene_description["integrator"]](self)

        self.intersectable_list = IntersectableList()
        self.light_sources = []

        self.build_intersectables(object_params_list=scene_description["objects"])
        self.build_light_sources(light_params_list=scene_description["lights"])

    def build_camera(self, camera_params) -> Camera:
        eye = Vec3(*camera_params["eye"])
        look_at = Vec3(*camera_params["look_at"])
        up = Vec3(*camera_params["up"])
        aspect_ratio = self.width / self.height

        return Camera(
            eye=eye,
            look_at=look_at,
            up=up,
            fov=camera_params["fov"],
            aspect_ratio=aspect_ratio,
            width=self.width,
            height=self.height
        )

    def build_intersectables(self, object_params_list):
        for sphere_params in object_params_list["spheres"]:
            material_type = list(sphere_params["material"])[0]
            material_params = sphere_params["material"][material_type]
            sphere = Sphere(
                material=self.MATERIALS[material_type](material_params),
                center=Vec3(*sphere_params["center"]),
                radius=sphere_params["radius"]
            )
            self.intersectable_list.append(sphere)

        for plane_params in object_params_list["planes"]:
            material_type = list(plane_params["material"])[0]
            material_params = plane_params["material"][material_type]
            plane = Plane(
                material=self.MATERIALS[material_type](material_params),
                normal=Vec3(*plane_params["normal"]),
                distance=plane_params["distance"]
            )
            self.intersectable_list.append(plane)

    def build_light_sources(self, light_params_list):
        for light_params in light_params_list:
            light_type = list(light_params)[0]
            params = light_params[light_type]
            self.light_sources.append(
                self.LIGHT_TYPES[light_type](params)
            )
