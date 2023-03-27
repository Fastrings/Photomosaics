import cv2 as cv
import numpy as np

def avg_color_of_squares(img):

    # Define size of grid squares
    square_size = 10  

    # Compute average color for each grid square
    avg_colors = []
    for y in range(0, img.shape[0], square_size):
        row_colors = []
        for x in range(0, img.shape[1], square_size):
            # Extract square from image
            square = img[y:y+square_size, x:x+square_size]
            # Compute average color of square
            avg_color = np.mean(square, axis=(0, 1))
            row_colors.append(avg_color)
        avg_colors.append(row_colors)

    # Print average colors for each grid square
    print("Average colors:")
    for row in avg_colors:
        for color in row:
            print(color, end=' ')
        print()

def pixellate(img):

    # Pixellation 'intensity'
    square_size = 20

    for y in range(0, img.shape[0], square_size):
        for x in range(0, img.shape[1], square_size):
            # Compute bounds of square
            y1, y2 = y, min(y + square_size, img.shape[0])
            x1, x2 = x, min(x + square_size, img.shape[1])
            # Compute average color of square
            square = img[y1:y2, x1:x2]
            avg_color = tuple(np.round(np.mean(square, axis=(0, 1))))
            # Set color of square to average color
            img[y1:y2, x1:x2] = avg_color
    
    # Display image
    cv.imshow("Image", img)
    cv.waitKey(0)
    cv.destroyAllWindows()

def avg_color_of_img(img):
    r_total = 0
    g_total = 0
    b_total = 0
    n_pixels = 0
    for row in img:
        for p in row:
            r_total += p[0]
            g_total += p[1]
            b_total += p[2]

            n_pixels += 1

    return (r_total / n_pixels, g_total / n_pixels, b_total / n_pixels)