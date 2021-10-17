import shutil
import sys
from pathlib import Path

import cv2
import matplotlib.image as mpt_img
import numpy as np
import yaml
from PIL import Image

from utils import ensure_dir

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


def average_brightness(rgb_image):
    """
    Calculates the average brightness of a given image.

    :param rgb_image: input image
    :return: average brightness value
    """
    # Convert image to HSV
    hsv = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2HSV)

    # Add up all the pixel values in the V channel
    sum_brightness = np.sum(hsv[:, :, 2])
    area = rgb_image.shape[0] * rgb_image.shape[1]

    # Find the avg
    avg = sum_brightness / area

    return avg


def slow_horizontal_variance(image_path):
    """
    Calculates average variance of horizontal lines of a grayscale image

    :param image_path: input image path
    :return: average horizontal variance
    """
    im = Image.open(image_path).convert('L')
    width, height = im.size
    if not width or not height:
        return 0
    variance = []
    pix = im.load()
    for y in range(height):
        row = [pix[x, y] for x in range(width)]
        mean = sum(row) / width
        h_variance = sum([(x - mean) ** 2 for x in row]) / width
        variance.append(h_variance)
    return sum(variance) / height


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
