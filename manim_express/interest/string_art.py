#!/usr/bin/python

import math
import sys
import numpy as np
import cv2
import time


def bresenham(x0, y0, x1, y1):
    """
    Bresenham-like algorithm returns coords for 4-connected lines.
    Resource: https://stackoverflow.com/questions/5186939/algorithm-for-drawing-a-4-connected-line

    Parameters:
    x0, y0 (int): x, y coords of first point
    x1, y1 (int): x, y coords of second point

    Returns: All coordinates along a line between two given points.
    """
    dx = abs(x1 - x0)  # distance to travel in X
    dy = abs(y1 - y0)  # distance to travel in Y

    if x0 < x1:
        ix = 1  # x will increase at each step
    else:
        ix = -1  # x will decrease at each step

    if y0 < y1:
        iy = 1  # y will increase at each step
    else:
        iy = -1  # y will decrease at each step

    e = 0  # Current error

    for i in range(dx + dy):
        yield (x0, y0)
        e1 = e + dy
        e2 = e - dx
        if abs(e1) < abs(e2):
            # Error will be smaller moving on X
            x0 += ix
            e = e1
        else:
            # Error will be smaller moving on Y
            y0 += iy
            e = e2


def get_pin_list(center=(0, 0), r=150, n=200):
    """
    Calculates coordinates for each pin on the image.

    Parameters:
    center (int, int): coordinates for center of the image.
    r (int): radius of circle.
    n (int): number of pins.

    Returns: Array of coordinates for each pin.
    """
    points = np.array(
        [[int(center[0] + math.cos(np.pi * 2 * i / n) * r), int(center[1] + math.sin(np.pi * 2 * i / n) * r)] for i in
         range(n)])
    return points


def pins_too_close(pinA, pinB):
    """
    Checks if chosen pins are too close on loom.

    Parameters:
    pinA (int): starting pin.
    pinB (int): ending pin.

    Returns: True if pins too close.
    """
    if abs(pinA - pinB) < 25:
        return True


def show_image(string_art, thread_count, num_lines, square):
    """
    Shows the threaded image as it is built to the user in a GUI window.

    Parameters:
    string_art (np array): threaded image in-progress.
    thread_count (int): counter to show number of lines drawn on image.
    num_lines (int): number of lines that will be used to create image.
    square (int): width x height dimensions of image.

    Returns: None
    """
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', square, square)
    cv2.putText(string_art, str(thread_count - 1), (900, 900), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)
    cv2.putText(string_art, str(thread_count), (900, 900), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2)
    if thread_count == num_lines:
        cv2.putText(string_art, str(thread_count), (900, 900), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)
    cv2.imshow('image', string_art)
    cv2.waitKey(1)


def update_image(pinX, pinY, image, string_art):
    """
    Applies a mask to the original image and does a bitwise OR to update pixel data.
    Note: mask about 30 sec faster than accessing each pixel individually and updating value.

    Parameters:
    pinX (tuple): coords of starting pin
    pinY (tuple): coords of ending pin
    image (np array): original image
    string_art (np array): threaded image in-progress.

    Returns: original image updated with white line drawn. Result image updated with black line drawn.
    """
    mask = np.zeros(image.shape[:2], dtype="uint8")
    cv2.line(mask, pinX, pinY, 255, 1)
    cv2.line(string_art, pinX, pinY, 0, 1)
    image = cv2.bitwise_or(image, mask)

    return image


def add_frame(string_art, pin_list):
    """
    Draws tiny circles to represent where the pins on the image. Just for fun.

    Parameters:
    pin_list(np array): contains coordinates of all the pins.
    string_art (np array): the threaded image.

    Returns: The finished threaded image with drawn on pins.
    """
    for pin in pin_list:
        x, y = pin
        cv2.circle(string_art, (x, y), 3, (0, 0, 0), -1)
    return string_art


def main():
    start_time = time.time()

    # convert image to greyscale, crop, and resize
    orig_img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
    height, width = orig_img.shape[:2]
    smaller_dim = min(height, width)
    x1 = int((width - smaller_dim) / 2)
    y1 = int((height - smaller_dim) / 2)
    x2 = x1 + smaller_dim
    y2 = y1 + smaller_dim
    crop_img = orig_img[y1:y2, x1:x2]
    radius = 500
    square = 2 * radius + 1
    image = cv2.resize(crop_img, (square, square))
    # cv2.imwrite(sys.argv[1].split('.')[0] + '_cropped.png', image)

    height, width = image.shape[:2]
    string_art = 255 * np.ones((height, width))
    num_pins = 200

    # allow user to specify number of lines used, or default to 1000 lines
    try:
        num_lines = int(sys.argv[2])
    except IndexError:
        num_lines = 1000

    center_x = int(width / 2)
    center_y = int(height / 2)

    pin_list = get_pin_list(center=(center_x, center_y), r=radius, n=num_pins)

    start_pin = 0
    thread_count = 0
    print_list = []
    print
    "Creating threaded image of " + sys.argv[1] + " with " + str(num_lines) + " threads. Please wait...\n"

    for line in range(num_lines):
        darkest_line = float("inf")
        start_coords = pin_list[start_pin]

        for pin in range(1, num_pins):
            end_pin = (start_pin + pin) % num_pins
            end_coords = pin_list[end_pin]

            if pins_too_close(start_pin, end_pin):
                continue

            line_coords = list(bresenham(start_coords[0], start_coords[1], end_coords[0], end_coords[1]))

            # unzip the list to get x, y coords separately
            pinX, pinY = zip(*line_coords)
            pixel_sum = np.sum(image[pinY, pinX])
            line_avg = int(pixel_sum / len(line_coords))

            # darker<--[0..255]-->lighter
            if line_avg < darkest_line:
                next_pin = end_pin
                darkest_line = line_avg

        thread_count += 1
        print_list.append((start_pin, next_pin))
        image = update_image(tuple(pin_list[start_pin]), tuple(pin_list[next_pin]), image, string_art)
        # UNCOMMENT the below line to view image in-progress
        # show_image(string_art, thread_count, num_lines, square)
        start_pin = next_pin

    string_art = add_frame(string_art, pin_list)
    cv2.imwrite(sys.argv[1].split('.')[0] + '_results.png', string_art)
    print("Finished: " + sys.argv[1].split('.')[0] + "_results.png")
    print(
        int(time.time() - start_time), "seconds elapsed.")
    # UNCOMMENT the below lines to view image when complete in GUI.
    # cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('image', square, square)
    # cv2.imshow('image', string_art)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # UNCOMMENT the below lines to print pin-to-pin instructions to text file.
    # write_file = open("instructions.txt", "w")
    # for coord in print_list:
    #     x, y = coord
    #     write_file.writelines(str(x) + " --> " + str(y) + "\n")
    # write_file.close()


if __name__ == "__main__":
    main()
