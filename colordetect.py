import numpy as np
import cv2 as cv

# Define color ranges in HSV for Rubik's Cube colors
COLOR_RANGES = {
    "Y": [(20, 50, 50), (30, 255, 255)],
    "W": [(0, 0, 200), (180, 30, 255)],
    "O": [(10, 50, 50), (19, 255, 255)],  # Ridotto il limite superiore
    "G": [(31, 50, 50), (80, 255, 255)],
    "B": [(100, 50, 50), (140, 255, 255)],
}

# Add a special case for red to handle the wraparound
RED_RANGES = [
    [(0, 50, 50), (9, 255, 255)],  # Lower range for red
    [(170, 50, 50), (180, 255, 255)],  # Upper range for red
]

def categorize_color(roi):
    # Convert ROI to HSV
    hsv_roi = cv.cvtColor(roi, cv.COLOR_BGR2HSV)

    # Calculate the average color of the ROI
    avg_color = np.mean(hsv_roi, axis=(0, 1))  # Average over rows and columns

    # Special handling for red (unify the two ranges)
    if (0 <= avg_color[0] <= 9 or 170 <= avg_color[0] <= 180) and avg_color[1] >= 50 and avg_color[2] >= 50:
        return "R"

    # Check other colors
    for color, (lower, upper) in COLOR_RANGES.items():
        lower = np.array(lower, dtype=np.uint8)
        upper = np.array(upper, dtype=np.uint8)

        # Check if the average color is within the range
        if lower[0] <= avg_color[0] <= upper[0] and lower[1] <= avg_color[1] <= upper[1] and lower[2] <= avg_color[2] <= upper[2]:
            return color

    return " "  # If no match is found