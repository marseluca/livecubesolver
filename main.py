import numpy as np
import cv2 as cv
import squarecontours as sc
import assemblecube as cube
import cubesolver as solver
import detectcolor
import webview
import launchcube

# Set up camera and frame size
cam = cv.VideoCapture(0)
screen_resolution = 1280, 720
frame_x, frame_y = int(screen_resolution[0] / 4), int(screen_resolution[1] / 4)
frame_w, frame_h = frame_x + (2 * frame_x), frame_y + (2 * frame_y)

cube_config = {
    'U': None,
    'F': None,
    'L': None,
    'D': None,
    'R': None,
    'B': None
}
face_count = 1

for i in range(6):
    print("\nScanning face ", face_count, " - Press [q] to save the configuration")

    while True:
        
        # Get frame from webcam
        check, image = cam.read()
        
        # Crop the frame
        image = image[frame_y:frame_h, frame_x:frame_w]

        # Make the image gray
        gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        # Canny frame without noise
        noiseless_image = cv.fastNlMeansDenoising(gray_image, None, 20, 7, 7)
        blurred_image = cv.blur(noiseless_image, (3, 3))
        canny_image = cv.Canny(blurred_image, 30, 200)
        dilated_image = cv.dilate(canny_image, cv.getStructuringElement(cv.MORPH_RECT, (9, 9)))

        # Find contours
        contours, hierarchy = cv.findContours(dilated_image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        # Stores contours with the right dimensions and colours
        square_contours = []

        # Copy the original image to draw contours on it
        im2 = image.copy()
        for contour in contours:
            # Approximate the contour
            approx = cv.approxPolyDP(contour, 0.1 * cv.arcLength(contour, True), True)

            # Filter based on the number of vertices
            if len(approx) == 4:  # Only consider contours with 4 vertices
                # Get dimensions of the contour and calculate w/h ratio and area
                x, y, w, h = cv.boundingRect(approx)
                ratio = float(w) / h
                area = cv.contourArea(approx)

                if ratio >= 0.7 and ratio <= 1.3 and w <= 70 and area >= 900:
                    # Draw the approximated contour on the image

                    # Extract the frame delimited by the contour
                    roi = image[y:y+h, x:x+w]  # Crop the region of interest
                    
                    # Categorize the color of the ROI
                    # color = cdetect.categorize_color(roi)
                    color = detectcolor.detect_color(roi)
                    square_contours.append({"x": x, "y": y, "w": w, "h": h, "colour": color})
        
        # Process the square contours (if needed)
        processed_contours = sc.process_square_contours(square_contours)

        # Confronta i nuovi colori con quelli precedenti
        if processed_contours:

            detected_colors = [contour["colour"] for contour in processed_contours]

            # Disegna i colori sulla webcam
            im2 = sc.draw_processed_contours(im2, processed_contours)

        # Show the image with detected contours on the webcam feed
        cv.imshow('Rubik\'s Cube Detection', im2)

        key = cv.waitKey(1) & 0xFF
        if key == ord('q'):  # Print the processed contours
            while True:  # Ripeti finché tutte le componenti di detected_colors non sono valide

                
                face = detected_colors[4]  # Middle square color
                face = cube.get_face(face)
                print("Face ", face)
        

                if all(color != " " for color in detected_colors):
                    # Get current face

                    # Update corresponding configuration
                    print("Configuration: ", detected_colors)
                    cube_config = cube.update_face_mapping(cube_config, face, detected_colors)
                    
                    face_count = face_count + 1
                    break
                else:
                    print("Detected colors contain empty values. Please try again.")
                    break
            break

# print(cube_config)

# Release the camera, writer, and close all windows
cam.release()
cv.destroyAllWindows()

# Convert configuration to AnimCubeJS format
animcube_string = cube.assemble_animcube_string(cube_config)
# print("AnimCubeJS Config: ",animcube_string)

# Compute solution string
solver_string = cube.assemble_solver_string(cube_config)
solution = solver.solve_cube(solver_string)

# Apply solution to AnimCubeJS
solution_content = launchcube.convert_moves(solution)
launchcube.update_animcube_config(animcube_string,solution_content)
print("\nSolution: ", solution_content)

# Launch AnimCubeJS
anim_cube_js_location = 'file:///C:/Users/Luca/Desktop/rubiks%20cube%20project/main.html'
window = webview.create_window("CV Project by Luca Marseglia", anim_cube_js_location, width=350, height=400, resizable=False)
webview.start()