import shutil
import sys
from pathlib import Path

import matplotlib.image as mpt_img
import yaml

from utils import ensure_dir, average_brightness, slow_horizontal_variance

params = yaml.safe_load(open("params.yaml"))["classify_day_night_and_foggy_images"]

if len(sys.argv) != 2:
    sys.stderr.write("Arguments error. Usage:\n")
    sys.stderr.write("\tpython3 classify_day_night_and_foggy_images.py input-data-directory\n")
    sys.exit(1)

input_directory = sys.argv[1]
day_night_image_threshold = params["day_night_image_threshold"]
fog_image_threshold = params["fog_image_threshold"]
output_directories = (Path("data", "outputs", "day_images", "foggy"),
                      Path("data", "outputs", "day_images", "sharp"),
                      Path("data", "outputs", "night_images", "foggy"),
                      Path("data", "outputs", "night_images", "sharp"))


def classify_day_night_and_foggy_images(input_dir, output_dirs):
    """
    Calculates the average brightness and average horizontal variance of of all the image in the input directory.
    Then moves them to different directories based on the output directories.

    :param input_dir: path to the input directory
    :param output_dirs: list of paths to the output directories
    :return:
    """
    for directory in output_dirs:
        ensure_dir(directory)
    for input_file in Path(input_dir).glob('*'):
        img = mpt_img.imread(input_file)
        avg_img_brightness = average_brightness(img)
        horizontal_variance = slow_horizontal_variance(input_file)
        if avg_img_brightness > day_night_image_threshold and horizontal_variance < fog_image_threshold:
            print(f"image {input_file.name} is day and foggy")
            output_file = output_directories[0].joinpath(input_file.name)
            shutil.copy(input_file, output_file)
        elif avg_img_brightness > day_night_image_threshold and horizontal_variance > fog_image_threshold:
            print(f"image {input_file.name} is day and sharp")
            output_file = output_directories[1].joinpath(input_file.name)
            shutil.copy(input_file, output_file)
        elif avg_img_brightness < day_night_image_threshold and horizontal_variance < fog_image_threshold:
            print(f"image {input_file.name} is night and foggy")
            output_file = output_directories[2].joinpath(input_file.name)
            shutil.copy(input_file, output_file)
        elif avg_img_brightness < day_night_image_threshold and horizontal_variance > fog_image_threshold:
            print(f"image {input_file.name} is night and sharp")
            output_file = output_directories[3].joinpath(input_file.name)
            shutil.copy(input_file, output_file)
        else:
            raise Exception(f"Image {input_file.name} with average brightness {avg_img_brightness} and horizontal "
                            f"variance {horizontal_variance}, could not be classified")


if __name__ == '__main__':
    classify_day_night_and_foggy_images(input_directory, output_directories)
