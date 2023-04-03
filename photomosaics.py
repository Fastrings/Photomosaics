import cv2 as cv
import numpy as np
import os, sys
import multiprocessing

library_path = "Source_Images"
cache = {}
num_processes = 4

def load_image(file_path):
    return cv.imread(file_path, cv.IMREAD_UNCHANGED)

def load_library(tile_size):
    pool = multiprocessing.Pool(processes=num_processes)
    file_paths = [os.path.join(library_path, file_name) for file_name in os.listdir(library_path)]
    images = pool.map(load_image, file_paths)
    pool.close()
    pool.join()

    library = {os.path.basename(file_path): cv.resize(image, (tile_size, tile_size)) for file_path, image in zip(file_paths, images)}

    return library

def photomosaics(img, tile_size):
    img = cv.resize(img, (img.shape[1] - (img.shape[1] % tile_size), img.shape[0] - (img.shape[0] % tile_size)))
    
    """library = {file_name: cv.resize(cv.imread(os.path.join(library_path, file_name), cv.IMREAD_UNCHANGED), (tile_size, tile_size))
               for file_name in os.listdir(library_path)}"""
    
    library = load_library(tile_size)
    
    if not library:
        print("Error: Image library is empty.")
        exit()
    
    cache = {file_name: np.mean(image, axis=(0, 1)) for file_name, image in library.items()}
    
    output_image = np.zeros_like(img)

    for y in range(0, img.shape[0], tile_size):
        for x in range(0, img.shape[1], tile_size):
            tile = img[y:y+tile_size, x:x+tile_size]
            tile_avg_color = np.mean(tile, axis=(0, 1)).astype(int)
            best_match = min(cache, key=lambda x: np.linalg.norm(tile_avg_color - cache[x]))
            best_match_image = library[best_match]
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