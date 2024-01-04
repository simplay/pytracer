from dataclasses import dataclass
from typing import List

from pytracer.math.vec3 import Vec3


@dataclass
class MeshData:
    vertices: List[Vec3]
    normals: List[Vec3]
    faces: List[Vec3]
    normal_faces: List[Vec3]


class ObjReader:
    """
    https://en.wikipedia.org/wiki/Wavefront_.obj_file
    """

    @staticmethod
    def read(filepath: str) -> MeshData:
        with open(filepath) as file:
            lines = [line.rstrip('\n') for line in file]

        vertices = []
        normals = []
        faces = []
        normal_faces = []

        prefixes = set()
        for line in lines:
            prefix, *rest = line.split(" ")
            prefixes.add(prefix)
            match prefix:
                case 'v':
                    vx, vy, vz, *_ = [float(item) for item in rest]
                    v = Vec3(vx, vy, vz)
                    vertices.append(v)
                case 'vn':
                    nx, ny, nz, *_ = [float(item) for item in rest]
                    normal = Vec3(nx, ny, nz).normalized()
                    normals.append(normal)
                case 'f':
                    f1, f2, f3, *_ = [int(item.split("//")[0]) for item in rest[1:]]
                    fn1, fn2, fn3, *_ = [int(item.split("//")[1]) for item in rest[1:]]
                    face = Vec3(f1, f2, f3)
                    normal_face = Vec3(fn1, fn2, fn3)

                    faces.append(face)
                    normal_faces.append(normal_face)

        return MeshData(
            vertices=vertices,
            normals=normals,
            faces=faces,
            normal_faces=normal_faces
        )
