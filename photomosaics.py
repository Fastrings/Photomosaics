import cv2 as cv
import numpy as np
import os, sys

TILE_SIZE = 25
library, library_path = {}, "Source_Images"
cache = {}


def photomosaics(filename):
    img = cv.imread(filename)
    img = cv.resize(img, (img.shape[1] - (img.shape[1] % TILE_SIZE), img.shape[0] - (img.shape[0] % TILE_SIZE)))

    for file_name in os.listdir(library_path):
        img_path = os.path.join(library_path, file_name)
        image = cv.imread(img_path)
        library[file_name] = cv.resize(image, (TILE_SIZE, TILE_SIZE))
    
    if not library:
        print("Error: Image library is empty.")
        exit()
    
    for file_name in library:
        cache[file_name] = np.mean(library[file_name], axis=(0, 1)).astype(int)
    
    output_image = np.zeros_like(img)

    for y in range(0, img.shape[1], TILE_SIZE):
        for x in range(0, img.shape[0], TILE_SIZE):
            tile = img[y:y+TILE_SIZE, x:x+TILE_SIZE]
            tile_avg_color = np.mean(tile, axis=(0, 1)).astype(int)
            best_match = min(cache, key=lambda x: np.linalg.norm(tile_avg_color - cache[x]))
            best_match_image = library[best_match]
            output_image[y:y+TILE_SIZE, x:x+TILE_SIZE] = best_match_image
    
    return output_image

if __name__ == "__main__":
    img = photomosaics(sys.argv[1])
    cv.imshow('output Image', img)
    cv.waitKey(0)
    cv.destroyAllWindows()