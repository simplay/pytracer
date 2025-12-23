import logging

from PIL import Image
import numpy as np
import multiprocessing
from multiprocessing import Pool
from threading import Timer
import time
import random
import ctypes
import os

from pytracer import RenderTask
from pytracer import Scene


def init_shared_state(
        n,
        shared_array_base_red,
        shared_array_base_green,
        shared_array_base_blue,
        shared_array_base_red_count,
        shared_array_base_green_count,
        shared_array_base_blue_count,
        raw_shared_status
):
    """ store pixels for later use """

    global pixels_red
    global pixels_green
    global pixels_blue

    global pixel_red_count
    global pixel_green_count
    global pixel_blue_count

    global shared_status

    pixels_red = np.ctypeslib.as_array(shared_array_base_red.get_obj())
    pixels_green = np.ctypeslib.as_array(shared_array_base_green.get_obj())
    pixels_blue = np.ctypeslib.as_array(shared_array_base_blue.get_obj())

    pixel_red_count = np.ctypeslib.as_array(shared_array_base_red_count.get_obj())
    pixel_green_count = np.ctypeslib.as_array(shared_array_base_green_count.get_obj())
    pixel_blue_count = np.ctypeslib.as_array(shared_array_base_blue_count.get_obj())

    shared_status = np.ctypeslib.as_array(raw_shared_status.get_obj())
    for idx in range(n):
        shared_status[idx] = 0


def compute_contribution(render_task: RenderTask) -> RenderTask:
    # perform actual computations here...
    for idx in render_task.indices:
        samples = render_task.scene.sampler.make_sample(render_task.spp, 2)

        for sample in samples:
            #  compute 2D image lookup coordinates (rowIdx, colIdx) from 1D index value
            row_idx = idx // render_task.width
            col_idx = idx % render_task.width

            ray = render_task.scene.camera.make_worldspace_ray(row_idx, col_idx, sample)
            spectrum = render_task.scene.integrator.integrate(ray)

            pixels_red[idx] += spectrum[0]
            pixels_green[idx] += spectrum[1]
            pixels_blue[idx] += spectrum[2]

            pixel_red_count[idx] += 1
            pixel_green_count[idx] += 1
            pixel_blue_count[idx] += 1

        shared_status[idx] = 1

    return render_task


class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


class Renderer:
    channels = 3

    def __init__(self, scene: Scene, output_filename: str):
        self.scene = scene
        self.width = scene.width
        self.height = scene.height
        self.output_filename = output_filename

    @staticmethod
    def compute_indices_groups(index_count: int, cpu_count: int) -> np.array:
        indices = range(index_count)
        indices = [idx for idx in indices]
        random.shuffle(indices)
        return np.array_split(indices, cpu_count)

    def write_image(self, output_filename, red: list, blue: list, green: list):
        start_time = time.time()
        img_data = np.zeros((self.height, self.width, self.channels), dtype=np.uint8)

        # Set the RGB values
        for y in range(img_data.shape[0]):
            for x in range(img_data.shape[1]):
                r, g, b = red[y][x], green[y][x], blue[y][x]

                if r > 1:
                    r = 1.0
                if g > 1:
                    g = 1.0
                if b > 1:
                    b = 1.0

                img_data[y][x][0] = r * 255
                img_data[y][x][1] = g * 255
                img_data[y][x][2] = b * 255

        end_time = time.time()

        output_image = Image.fromarray(img_data)

        project_root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        filename = f"{output_filename}.png"
        filepath = os.path.join(project_root_path, 'output', filename)
        logging.info(f"Wrote image {filepath} in {end_time - start_time} seconds")
        output_image.save(filepath)

    def render(self, spp: int, thread_count: int = None) -> None:
        """
        @param spp [int] samples per pixel
        @param thread_count the number of threads used to render the image. By default, the total number of available threads is used.
        """
        cpu_count = thread_count or multiprocessing.cpu_count()
        logging.info(f"Starting {cpu_count} threads")
        index_groups = self.compute_indices_groups(index_count=self.width * self.height, cpu_count=cpu_count)

        tasks = []
        for idx in range(0, cpu_count):
            tasks.append(RenderTask(scene=self.scene, indices=index_groups[idx], spp=spp))

        n = self.height * self.width
        shared_array_base_red = multiprocessing.Array(ctypes.c_double, n)
        shared_array_base_green = multiprocessing.Array(ctypes.c_double, n)
        shared_array_base_blue = multiprocessing.Array(ctypes.c_double, n)

        shared_array_base_red_count = multiprocessing.Array(ctypes.c_int, n)
        shared_array_base_green_count = multiprocessing.Array(ctypes.c_int, n)
        shared_array_base_blue_count = multiprocessing.Array(ctypes.c_int, n)

        raw_shared_status = multiprocessing.Array(ctypes.c_int, n)

        def show_progress():
            completed_task_count = np.sum(raw_shared_status)
            percentage = int(100 * (completed_task_count / n))
            logging.info(f"=> Progress: {str(percentage)}% ")

        timer = RepeatTimer(1, show_progress)
        timer.start()

        start_time = time.time()
        with Pool(
                processes=cpu_count,
                initializer=init_shared_state,
                initargs=(
                        n,
                        shared_array_base_red,
                        shared_array_base_green,
                        shared_array_base_blue,
                        shared_array_base_red_count,
                        shared_array_base_green_count,
                        shared_array_base_blue_count,
                        raw_shared_status

                )) as pool:
            pool.map(compute_contribution, tasks)

        end_time = time.time()
        timer.cancel()
        show_progress()
        logging.info(f"Completed raytracing in {end_time - start_time} seconds")

        new_shape = (self.height, self.width)

        red = np.reshape(np.frombuffer(shared_array_base_red.get_obj()), newshape=new_shape)
        green = np.reshape(np.frombuffer(shared_array_base_blue.get_obj()), newshape=new_shape)
        blue = np.reshape(np.frombuffer(shared_array_base_green.get_obj()), newshape=new_shape)

        red_count = np.reshape(
            np.frombuffer(shared_array_base_red_count.get_obj(), dtype='int32'),
            newshape=new_shape
        ) + 1e-8

        green_count = np.reshape(
            np.frombuffer(shared_array_base_green_count.get_obj(), dtype='int32'),
            newshape=new_shape
        ) + 1e-8

        blue_count = np.reshape(
            np.frombuffer(shared_array_base_blue_count.get_obj(), dtype='int32'),
            newshape=new_shape
        ) + 1e-8

        red = red / red_count
        green = green / green_count
        blue = blue / blue_count

        self.write_image(self.output_filename, red, green, blue)
