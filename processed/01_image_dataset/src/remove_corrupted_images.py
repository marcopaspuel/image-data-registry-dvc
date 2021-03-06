import shutil
import sys
from pathlib import Path

from PIL import Image

from utils import ensure_dir

if len(sys.argv) != 2:
    sys.stderr.write("Arguments error. Usage:\n")
    sys.stderr.write("\tpython3 remove_corrupted_images.py input-data-directory\n")
    sys.exit(1)

input_directory = sys.argv[1]
output_directory = Path("data", "intermediate", "remove_corrupted_images")


def remove_corrupted_images(input_dir, output_dir):
    """
    Opens all the files of a given directory and verifies if they are valid images.
    If it is an image it copies the file to the output directory.

    :param input_dir: path to the input directory
    :param output_dir: path to the output directory
    :return:
    """
    ensure_dir(output_dir)
    for input_file in Path(input_dir).glob('**/*'):
        try:
            img = Image.open(input_file)  # open the image file
            img.verify()  # verify that it is, in fact an image
            print(str(input_file.name) + " OK")

            output_file = output_dir.joinpath(input_file.name)
            shutil.copy(input_file, output_file)

        except (IOError, SyntaxError) as e:
            print('Bad file:', input_file.name)  # Print out the names of corrupt files


if __name__ == '__main__':
    remove_corrupted_images(input_directory, output_directory)
