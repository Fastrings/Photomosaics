import cv2 as cv
import numpy as np
import os, sys
from scipy.spatial import KDTree
import colorspacious
import argparse

LIBRARY_PATH = "Source_Images"

def color_distance(color1, color2):
    col1 = [color1[0], color1[1], color1[2]]
    col2 = [color2[0], color2[1], color2[2]]
    col1_lab = colorspacious.cspace_convert(col1, "sRGB255", "CAM02-UCS")
    col2_lab = colorspacious.cspace_convert(col2, "sRGB255", "CAM02-UCS")

    return colorspacious.deltaE(col1_lab, col2_lab)

def find_best_match(color, kdtree, library):
    _, indices = kdtree.query(color)
    if isinstance(indices, np.int64):
        indices = [indices]
    best_match = None
    best_distance = float('inf')
    for index in indices:
        distance = color_distance(color, library[index]['average_color'])
        if distance < best_distance:
            best_match = library[index]
            best_distance = distance
    
    return best_match

def load_image(file_path, tile_size):
    img = cv.imread(file_path, cv.IMREAD_UNCHANGED)
    return cv.resize(img, (tile_size, tile_size))

def average_color(image):
    return cv.mean(image)[:3]

def load_library(tile_size):
    file_paths = [os.path.join(LIBRARY_PATH, file_name) for file_name in os.listdir(LIBRARY_PATH)]
    library = []
    for file_path in file_paths:
        image = load_image(file_path, tile_size)
        avg = average_color(image)
        library.append({'image': image, 'average_color': avg})

    return library

def photomosaics(img, tile_size):
    img = cv.resize(img, (img.shape[1] - (img.shape[1] % tile_size), img.shape[0] - (img.shape[0] % tile_size)))
    library = load_library(tile_size)
    colors = np.array([image_dict['average_color'] for image_dict in library])
    kdtree = KDTree(colors)

    if not library:
        raise Exception("Error: Image library is empty.")
    
    output_image = np.zeros_like(img)

    for y in range(0, img.shape[0], tile_size):
        for x in range(0, img.shape[1], tile_size):
            tile = img[y:y+tile_size, x:x+tile_size]
            tile_avg_color = average_color(tile)
            best_match = find_best_match(tile_avg_color, kdtree, library)
            best_match_image = best_match['image']
            output_image[y:y+tile_size, x:x+tile_size] = best_match_image
    
    return output_image

def display(input, output):
    input = cv.resize(input, (500, 500))
    output = cv.resize(output, (500, 500))

    cv.imshow('Result', output)
    cv.imshow('Input image', input)
    cv.moveWindow('Input image', 100, 50)
    cv.moveWindow('Result', 625, 50)
    cv.waitKey(0)
    cv.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a photomosaics program on input image.")

    parser.add_argument("-i", "--input", required=True, help="path to input image")
    parser.add_argument("-t", "--tile-size", type=int, required=True, help="size of tiles in output image")
    parser.add_argument("-m", "--method", choices=["euclid", "deltaE"], default='deltaE', help="color distance method to use")

    args = parser.parse_args()
    filename = args.input
    tile_size = args.tile_size
    method = color_distance if args.method == "deltaE" else None

    input_img = cv.imread(filename)
    img = photomosaics(input_img, tile_size)

    og = cv.imread(filename)

    display(og, img)