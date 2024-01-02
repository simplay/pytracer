import numpy as np

from pytracer.materials.material import Material
from pytracer.math.vec3 import Vec3
from pytracer.shading_sample import ShadingSample


class GridTexturedMaterial(Material):
    def __init__(self, line_color: Vec3, tile_color: Vec3, thickness: float, shift: Vec3, scale: float):
        from pytracer.materials.diffuse_material import DiffuseMaterial
        self.line_color = line_color
        self.tile_color = tile_color
        self.thickness = thickness
        self.shift = shift
        self.scale = scale
        self.diffuse = DiffuseMaterial(emission=Vec3(1.0, 1.0, 1.0))

    def evaluate_brdf(self, hit_record: 'HitRecord', w_out: Vec3, w_in: Vec3) -> Vec3:
        diffuse_brdf = self.diffuse.evaluate_brdf(hit_record, w_out, w_in)
        hit_position = Vec3.from_other(hit_record.position)
        shifted = Vec3.from_other(hit_record.position) + self.shift

        hit_position = hit_position / self.scale
        shifted = shifted / self.scale
        relative_thickness = self.thickness / self.scale

        rounded_position = Vec3.from_other(np.round(hit_position))

        shifted = shifted - rounded_position
        shifted = np.abs(shifted)

        sx, sy, sz = shifted[0], shifted[1], shifted[2]

        if sx < relative_thickness or sy < relative_thickness or sz < relative_thickness:
            diffuse_brdf *= self.line_color
        else:
            diffuse_brdf *= self.tile_color

        return diffuse_brdf

    def evaluate_emission(self, hit_record: 'HitRecord', w_out: Vec3) -> Vec3:
        return self.diffuse.evaluate_emission(hit_record, w_out)

    def has_specular_reflection(self) -> bool:
        return self.diffuse.has_specular_reflection()

    def has_specular_refraction(self) -> bool:
        return self.diffuse.has_specular_refraction()

    def does_cast_shadows(self) -> bool:
        return self.diffuse.does_cast_shadows()

    def evaluate_specular_reflection(self, hit_record: 'HitRecord') -> ShadingSample:
        return self.diffuse.evaluate_specular_reflection(hit_record)

    def evaluate_specular_refraction(self, hit_record: 'HitRecord') -> ShadingSample:
        return self.diffuse.evaluate_specular_refraction(hit_record)
