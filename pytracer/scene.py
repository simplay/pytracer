import json

from pytracer import Camera
from pytracer.integrators.debug_integrator import DebugIntegrator
from pytracer.intersectables.geometries.triangle import Triangle

from pytracer.materials.blinn_material import BlinnMaterial
from pytracer.integrators.whitted_integrator import WhittedIntegrator
from pytracer.materials.diffuse_material import DiffuseMaterial
from pytracer.intersectables.containers.intersectable_list import IntersectableList
from pytracer.one_sampler import OneSampler
from pytracer.intersectables.geometries.plane import Plane
from pytracer.light_sources.point_light import PointLight
from pytracer.materials.reflective_material import ReflectiveMaterial
from pytracer.materials.refractive_material import RefractiveMaterial
from pytracer.materials.grid_textured_material import GridTexturedMaterial
from pytracer.intersectables.geometries.sphere import Sphere
from pytracer.math.vec3 import Vec3

MATERIALS = {
    "blinn": lambda params: BlinnMaterial(diffuse=Vec3(*params["diffuse"]),
                                          specular=Vec3(*params["specular"]),
                                          shininess=params["shininess"]),
    "reflective": lambda params: ReflectiveMaterial(ks=Vec3(*params["ks"])),
    "refractive": lambda params: RefractiveMaterial(refraction_index=params["refraction_index"],
                                                    ks=Vec3(*params["ks"])),
    "diffuse": lambda params: DiffuseMaterial(emission=Vec3(*params["emission"])),
    "grid": lambda params: GridTexturedMaterial(line_color=Vec3(*params["line_color"]),
                                                tile_color=Vec3(*params["tile_color"]),
                                                thickness=params["thickness"],
                                                shift=Vec3(*params["shift"]),
                                                scale=params["scale"])
}

LIGHT_TYPES = {
    "point_light": lambda params: PointLight(position=Vec3(*params["position"]),
                                             emission=Vec3(*params["emission"]))
}

INTEGRATORS = {
    "whitted": WhittedIntegrator,
    "debug": DebugIntegrator
}


class Scene:
    def __init__(self, scene_filepath: str, width: int, height: int):
        with open(scene_filepath) as file:
            scene_description = json.load(file)

        self.width = width
        self.height = height

        self.camera = self.build_camera(camera_params=scene_description["camera"])
        self.sampler = OneSampler()
        self.integrator = INTEGRATORS[scene_description["integrator"]](self)

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
                material=MATERIALS[material_type](material_params),
                center=Vec3(*sphere_params["center"]),
                radius=sphere_params["radius"]
            )
            self.intersectable_list.append(sphere)

        for plane_params in object_params_list["planes"]:
            material_type = list(plane_params["material"])[0]
            material_params = plane_params["material"][material_type]
            plane = Plane(
                material=MATERIALS[material_type](material_params),
                normal=Vec3(*plane_params["normal"]),
                distance=plane_params["distance"]
            )
            self.intersectable_list.append(plane)

        for object_params in object_params_list["triangles"]:
            material_type = list(object_params["material"])[0]
            material_params = object_params["material"][material_type]
            intersectable = Triangle(
                material=MATERIALS[material_type](material_params),
                a=Vec3(*object_params["a"]),
                b=Vec3(*object_params["b"]),
                c=Vec3(*object_params["c"])
            )
            self.intersectable_list.append(intersectable)

    def build_light_sources(self, light_params_list):
        for light_params in light_params_list:
            light_type = list(light_params)[0]
            params = light_params[light_type]
            self.light_sources.append(
                LIGHT_TYPES[light_type](params)
            )
