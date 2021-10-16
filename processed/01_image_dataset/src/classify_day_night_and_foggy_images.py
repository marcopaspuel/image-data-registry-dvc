import shutil
import sys
from pathlib import Path

import cv2
import matplotlib.image as mpt_img
import numpy as np
import yaml

from utils import ensure_dir

params = yaml.safe_load(open("params.yaml"))["classify_day_night_and_foggy_images"]

if len(sys.argv) != 2:
    sys.stderr.write("Arguments error. Usage:\n")
    sys.stderr.write("\tpython3 classify_day_night_and_foggy_images.py input-data-directory\n")
    sys.exit(1)

input_directory = sys.argv[1]
day_night_image_threshold = params["day_night_image_threshold"]
foggy_image_threshold = params["foggy_image_threshold"]
day_imgs_output_dir = Path("data", "outputs", "day_images")
night_imgs_output_dir = Path("data", "outputs", "night_images")
foggy_imgs_output_dir = Path("data", "outputs", "foggy_images")


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


def classify_day_night_and_foggy_images(input_dir, day_output_dir, night_output_dir):
    """
    Calculates the average brightness of all the image in the input directory.
    If image is in between the brightness threshold, it copies the file to the output directory.

    :param input_dir: path to the input directory
    :param day_output_dir: path to the output directory
    :param night_output_dir: path to the output directory
    :return:
    """
    ensure_dir(day_output_dir)
    ensure_dir(night_output_dir)
    for input_file in Path(input_dir).glob('*'):
        img = mpt_img.imread(input_file)
        avg_img_brightness = average_brightness(img)
        if avg_img_brightness > day_night_image_threshold:
            print(f"image {input_file.name} is day with average brightness: {avg_img_brightness}")
            output_file = day_output_dir.joinpath(input_file.name)
            shutil.copy(input_file, output_file)
        elif avg_img_brightness < day_night_image_threshold:
            print(f"image {input_file.name} is night with average brightness: {avg_img_brightness}")
            output_file = night_output_dir.joinpath(input_file.name)
            shutil.copy(input_file, output_file)


if __name__ == '__main__':
    classify_day_night_and_foggy_images(input_directory, day_imgs_output_dir, night_imgs_output_dir)
