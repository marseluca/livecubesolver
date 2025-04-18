import cv2 as cv
import numpy as np

def process_square_contours(square_contours):
    """
    Process and sort square contours for a Rubik's Cube face.
    Args:
        square_contours (list): List of square contours with their properties.
    Returns:
        list: Processed and sorted square contours if valid, otherwise None.
    """
    if len(square_contours) != 9:
        return None

    # Sort on x-positions
    square_contours_sorted_x = sorted(square_contours, key=lambda item: item["x"])

    # Sort on y-positions - this will help deduce the three rows below
    square_contours_sorted_y = sorted(square_contours, key=lambda item: item["y"])

    # Define the top, middle and bottom rows
    sorted_rows = []
    for i in range(0, 9, 3):
        # These three items are in the same row
        unsorted_row = [square_contours_sorted_y[i], square_contours_sorted_y[i+1], square_contours_sorted_y[i+2]]
        
        # Sort on x-position and append
        sorted_rows.append(sorted(unsorted_row, key=lambda item: item["x"]))

    # Re-order the list of square contours using sequence above
    square_contours = sorted_rows[0] + sorted_rows[1] + sorted_rows[2]

    # Define the middle square so that we can use that as a reference point x, y, w, h
    middle_square = square_contours[4]

    # Find the square contours furthest to the left (x-min) and right (x-max)
    x_min = square_contours_sorted_x[0]
    x_max = square_contours_sorted_x[-1]

    # Find the square contours furthest to the top (y-min) and bottom (y-max)
    y_min = square_contours_sorted_y[0]
    y_max = square_contours_sorted_y[-1]

    # Need to avoid outlier contours that aren't on the Rubik's cube
    # Check the four contours at the extreme x-min, x-max, y-min, y-max are positioned close enough to the middle square
    gap_width = int(middle_square["w"] * 1.7)
    gap_height = int(middle_square["h"] * 1.7)

    if (middle_square["x"] - x_min["x"] <= gap_width and
        x_max["x"] - middle_square["x"] <= gap_width and
        middle_square["y"] - y_min["y"] <= gap_height and 
        y_max["y"] - middle_square["y"] <= gap_height):
        return square_contours

    return None


def draw_processed_contours(image, processed_contours):
    """
    Draws the processed contours on the given image and places the label at the center of each square.

    Args:
        image (numpy.ndarray): The image on which to draw the contours.
        processed_contours (list): A list of processed contours with their properties.
                                   Each contour should be a dictionary with keys like
                                   'x', 'y', 'w', 'h', and 'colour'.

    Returns:
        numpy.ndarray: The image with the contours drawn on it.
    """
    for contour in processed_contours:
        # Extract contour properties
        x, y, w, h = contour["x"], contour["y"], contour["w"], contour["h"]
        colour = contour["colour"]

        # Draw the rectangle around the contour
        cv.rectangle(image, (x, y), (x + w, y + h), (0, 0, 0), 2)

        # Calculate the center of the square
        center_x = x + w // 2
        center_y = y + h // 2

        # Put the color label at the center of the square
        cv.putText(image, colour, (center_x - 10, center_y + 5), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    return image