import shutil
import sys
from pathlib import Path

import matplotlib.image as mpt_img
import yaml

from utils import ensure_dir, average_brightness

params = yaml.safe_load(open("params.yaml"))["remove_dark_and_bright_images"]

if len(sys.argv) != 2:
    sys.stderr.write("Arguments error. Usage:\n")
    sys.stderr.write("\tpython3 remove_dark_and_bright_images.py input-data-directory\n")
    sys.exit(1)

input_directory = sys.argv[1]
dark_image_threshold = params["dark_image_threshold"]
bright_image_threshold = params["bright_image_threshold"]
output_directory = Path("data", "intermediate", "remove_dark_and_bright_images")


def remove_dark_and_bright_images(input_dir, output_dir):
    """
    Calculates the average brightness of all the image in the input directory.
    If image is in between the brightness threshold, it copies the file to the output directory.

    :param input_dir: path to the input directory
    :param output_dir: path to the output directory
    :return:
    """
    ensure_dir(output_dir)
    for input_file in Path(input_dir).glob('*'):
        img = mpt_img.imread(input_file)
        avg_img_brightness = average_brightness(img)
        if dark_image_threshold < avg_img_brightness < bright_image_threshold:
            output_file = output_dir.joinpath(input_file.name)
            shutil.copy(input_file, output_file)
        else:
            print(f"image {input_file.name} was removed with average brightness: {avg_img_brightness}")


if __name__ == '__main__':
    remove_dark_and_bright_images(input_directory, output_directory)
