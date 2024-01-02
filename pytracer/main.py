from pytracer import Scene
from pytracer import Renderer

from optparse import OptionParser

import os
import logging

from datetime import date
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent


def main():
    required_options = ["width", "height"]

    parser = OptionParser()
    parser.add_option(
        "-s",
        "--scene",
        dest="scene_filepath",
        help="Path to JSON file of scene that should be rendered",
        metavar="FILE"
    )

    parser.add_option(
        "-w",
        "--width",
        dest="width",
        type="int",
        help="With of rendered image"
    )

    parser.add_option(
        "-H",
        "--height",
        dest="height",
        type="int",
        help="Height of rendered image"
    )

    parser.add_option(
        "-p",
        "--spp",
        dest="spp",
        type="int",
        help="Samples per pixel",
        default=1
    )

    parser.add_option(
        "-q",
        "--quiet",
        action="store_false",
        dest="verbose",
        default=True,
        help="Do not print status messages to stdout"
    )

    (options, args) = parser.parse_args()

    for r in required_options:
        if options.__dict__[r] is None:
            parser.error("parameter %s is required" % r)

    today = date.today()
    current_date = today.strftime("%d_%m_%y")
    log_path = os.path.join(ROOT_PATH, 'logs', f"status_{current_date}.log")
    log_handlers = [
        logging.FileHandler(log_path, mode="a", encoding="utf8"),
    ]

    if options.verbose:
        log_handlers.append(
            logging.StreamHandler()
        )

    logging.basicConfig(
        handlers=log_handlers,
        format="%(asctime)s.%(msecs)03d | %(levelname)s | %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S",
        level=logging.DEBUG
    )

    scene_filepath = options.scene_filepath
    spp = options.spp
    logging.info(f"Starting rendering process using the following settings:")
    logging.info(f"  Scene: {scene_filepath}")
    logging.info(f"  Resolution: {options.width} x {options.height} pixels")
    logging.info(f"  Samples per pixel: {spp}")

    scene = Scene(scene_filepath=scene_filepath, width=options.width, height=options.height)
    renderer = Renderer(scene, output_filename="rendered_image")
    renderer.render(spp=spp)
    logging.info("Completed rendering")


if __name__ == '__main__':
    main()
