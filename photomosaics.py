import cv2 as cv
import numpy as np
import os, sys
from scipy.spatial import KDTree

LIBRARY_PATH = "Source_Images"

def color_distance(color1, color2):
    return np.sqrt(np.sum((np.array(color1) - np.array(color2)) ** 2))

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
        entry = {
            'image': load_image(file_path, tile_size),
            'average_color': None
        }
        library.append(entry)

    for image_dict in library:
        image_dict['average_color'] = average_color(image_dict['image'])

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

if __name__ == "__main__":
    input_img = cv.imread(sys.argv[1])
    img = photomosaics(input_img, int(sys.argv[2]))
    img = cv.resize(img, (500, 500))
    og = cv.imread(sys.argv[1])
    og = cv.resize(og, (500, 500))
    cv.imshow('Result', img)
    cv.imshow('Input image', og)
    cv.moveWindow('Input image', 100, 50)
    cv.moveWindow('Result', 625, 50)
    cv.waitKey(0)
    cv.destroyAllWindows()