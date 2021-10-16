import shutil
import sys
from pathlib import Path

import yaml
from PIL import Image

params = yaml.safe_load(open("params.yaml"))["remove_corrupted_images"]

input_dir = sys.argv[1]
output_dir = Path("data", "intermediate", "remove_corrupted_images")

print(input_dir)
print(output_dir)


def ensure_dir(directory):
    """
    Creates a directory if it does not exist yet.

    :param directory: path to directory to be created
    :return:
    """
    if not directory.is_dir():
        directory.mkdir()


def remove_corrupted_images(input_dir, output_dir):
    """
    Opens all the files of a given directory and verifies if they are valid images.
    If it is an image it copies the file to the output directory.

    :param input_dir: path to the input directory
    :param output_dir: path to the output directory
    :return:
    """
    ensure_dir(output_dir)
    for input_file in Path(input_dir).glob('*'):
        try:
            img = Image.open(input_file)  # open the image file
            img.verify()  # verify that it is, in fact an image
            print(str(input_file.name) + " OK")

            output_file = output_dir.joinpath(input_file.name)
            shutil.copy(input_file,
                        output_file)

        except (IOError, SyntaxError) as e:
            print('Bad file:', input_file.name)  # Print out the names of corrupt files


remove_corrupted_images(input_dir, output_dir)
