import numpy as np
import math

from pytracer.ray import Ray


# We define our camera by:
#  + the origin of the camera's eye (eye)
#  + a position in the scene at which the camera is looking at (lookAt) and a
#    vector
#  + that defines the relative upwards direction (up).
#
# An orthonormal basis M can be constructed by computing
#  w = (eye - lookAt) / norm(eye - lookAt)
#  u = cross_product(up, w) / norm(cross_product(up, w))
#  v = cross_product(w, u)
#  e = eye
#
# and setting M = [u, v, w, e]
#
#           v
#           |                fov / 2       . top
#          |                           .   |
#         |                        .       |
#   w ----e       =>            e----------| Image Plane
#        /                         .  w=-1 |
#       /                              .   |
#      u                                   . bottom
#
#  Camera coordinate System
#
# This matrix can be used to transform a point in camera coordinates into
# world coordinates, i.e.  p_xyz = M*p_uvw
#
# The viewing frustum defines the 3d volume that is projected within image
# boundaries and is defined by the vertical field-of-view and the aspect
# ratio.
class Camera:
    def __init__(self,
                 eye: np.ndarray,
                 look_at: np.ndarray,
                 up: np.ndarray,
                 fov: float,
                 aspect_ratio: float,
                 width: float,
                 height: float):
        self.eye = eye
        self.look_at = look_at
        self.up = up
        self.fov = fov
        self.aspect_ratio = aspect_ratio
        self.width = width
        self.height = height

        to = np.copy(look_at)
        w = (eye - to)
        w = w / np.linalg.norm(w)

        u = np.cross(up, w)
        u = u / np.linalg.norm(u)

        v = np.cross(w, u)

        self.matrix = np.array([
            [*u, 0.0],
            [*v, 0.0],
            [*w, 0.0],
            [*eye, 1.0]
        ])

        angular_fov = np.pi * (fov / 180.0)
        self.top = math.tan(angular_fov / 2.0)
        self.bottom = -self.top
        self.right = aspect_ratio * self.top
        self.left = -self.right

    #
    def make_worldspace_ray(self, i: int, j: int, samples: list) -> Ray:
        """
        Given a ray in image space, make a ray in world space according to the
        camera specifications. The method receives a sample that the camera can use
        to generate the ray. Typically, the first two sample dimensions are used to
        sample a location in the current pixel. The samples are assumed to be in
        the range [0,1].

        @param i row index, start counting at 0.
        @param j column index, start counting at 0
        @param samples random sample that the camera can use to generate a ray float array.
        @return the ray in world coordinates
        """

        s1, s2 = samples[0], samples[1]

        u_ij = self.left + (self.right - self.left) * (i + s1) / self.width
        v_ij = self.bottom + (self.top - self.bottom) * (j + s2) / self.height
        w_ij = -1.0

        v = np.array([u_ij, v_ij, w_ij, 0])
        p_uvw = self.matrix.dot(v)

        return Ray(self.eye.copy(), p_uvw, i, j, perturbate=False)
