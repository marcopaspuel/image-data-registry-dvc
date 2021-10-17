import cv2
import numpy as np
from PIL import Image


def ensure_dir(directory):
    """
    Creates a directory if it does not exist yet.

    :param directory: path to directory to be created
    :return:
    """
    if not directory.is_dir():
        directory.mkdir()


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
