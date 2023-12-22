from PIL import Image
import numpy as np
import multiprocessing
from multiprocessing import Pool
import time
import random
import ctypes
import os

from pytracer import RenderTask
from pytracer import Scene


class Renderer:
    channels = 3

    @staticmethod
    def init_shared_state(shared_array_base_red, shared_array_base_green, shared_array_base_blue):
        """ store pixels for later use """

        global pixels_red
        global pixels_green
        global pixels_blue

        pixels_red = np.ctypeslib.as_array(shared_array_base_red.get_obj())
        pixels_green = np.ctypeslib.as_array(shared_array_base_green.get_obj())
        pixels_blue = np.ctypeslib.as_array(shared_array_base_blue.get_obj())

    @staticmethod
    def compute_contribution(render_task: RenderTask) -> RenderTask:
        print(pixels_red)

        # perform actual computations here...
        for idx in render_task.indices:
            samples = render_task.scene.sampler.make_sample(render_task.spp, 2)
            print(samples)
            for sample in samples:
                #  compute 2D image lookup coordinates (rowIdx, colIdx) from 1D index value
                row_idx = idx / render_task.width
                col_idx = idx % render_task.width

                ray = render_task.scene.camera.make_worldspace_ray(row_idx, col_idx, sample)
                spectrum = render_task.scene.integrator.integrate(ray)

                pixels_red[idx] += spectrum[0]
                pixels_green[idx] += spectrum[1]
                pixels_blue[idx] += spectrum[2]

        print(render_task.indices)

        return render_task

    def __init__(self, scene: Scene):
        self.scene = scene
        self.width = scene.width
        self.height = scene.height

    @staticmethod
    def compute_indices_groups(index_count: int, cpu_count: int) -> np.array:
        indices = range(index_count)
        indices = [idx for idx in indices]
        random.shuffle(indices)
        return np.array_split(indices, cpu_count)

    def write_image(self, red, blue, green):
        start_time = time.time()
        img_data = np.zeros((self.height, self.width, self.channels), dtype=np.uint8)

        # Set the RGB values
        for y in range(img_data.shape[0]):
            for x in range(img_data.shape[1]):
                r, g, b = red[y][x], green[y][x], blue[y][x]
                img_data[y][x][0] = r * 255
                img_data[y][x][1] = g * 255
                img_data[y][x][2] = b * 255

        end_time = time.time()
        print(f"Computed image in {end_time - start_time} seconds")

        output_image = Image.fromarray(img_data)

        project_root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        filename = 'rendered-image.png'
        filepath = os.path.join(project_root_path, 'output', filename)
        output_image.save(filepath)

    def render(self, spp: int, thread_count: int = None) -> None:
        cpu_count = thread_count or multiprocessing.cpu_count()
        index_groups = self.compute_indices_groups(index_count=self.width * self.height, cpu_count=cpu_count)

        tasks = []
        for idx in range(0, thread_count):
            tasks.append(RenderTask(scene=self.scene, indices=index_groups[idx], spp=spp))

        n = self.height * self.width
        shared_array_base_red = multiprocessing.Array(ctypes.c_double, n)
        shared_array_base_green = multiprocessing.Array(ctypes.c_double, n)
        shared_array_base_blue = multiprocessing.Array(ctypes.c_double, n)

        start_time = time.time()
        with Pool(processes=cpu_count,
                  initializer=self.init_shared_state,
                  initargs=(
                          shared_array_base_red,
                          shared_array_base_green,
                          shared_array_base_blue
                  )) as pool:
            pool.map(self.compute_contribution, tasks)

        end_time = time.time()
        print(f"done in {end_time - start_time} seconds")

        new_shape = (self.height, self.width)
        red = np.reshape(shared_array_base_red, newshape=new_shape)
        green = np.reshape(shared_array_base_blue, newshape=new_shape)
        blue = np.reshape(shared_array_base_green, newshape=new_shape)

        self.write_image(red, green, blue)
