from pytracer.intersectables.containers.intersectable_list import IntersectableList
from pytracer.intersectables.geometries.triangle import MeshTriangle, Triangle
from pytracer.intersectables.obj_reader import ObjReader

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytracer import Material


class Mesh(IntersectableList):
    def __init__(self, material: 'Material', filepath: str, use_face_normals=False):
        super().__init__()

        mesh = ObjReader.read(filepath)

        for face_idx, face in enumerate(mesh.faces):
            id_x, id_y, id_z = face[0], face[1], face[2]
            vx = mesh.vertices[id_x - 1]
            vy = mesh.vertices[id_y - 1]
            vz = mesh.vertices[id_z - 1]

            if len(mesh.normals) > 0 and use_face_normals:
                normal_face = mesh.normal_faces[face_idx]

                id_nx, id_ny, id_nz = normal_face[0], normal_face[1], normal_face[2]

                nx = mesh.normals[id_nx - 1]
                ny = mesh.normals[id_ny - 1]
                nz = mesh.normals[id_nz - 1]

                triangle = MeshTriangle(material, vx, vy, vz, nx, ny, nz, face_idx)
                self.container.append(triangle)

            else:
                triangle = Triangle(material, vx, vy, vz, face_idx)
                self.container.append(triangle)
