import cv2 as cv
import numpy as np
import os, sys

library, library_path = {}, "Source_Images"
cache = {}


def photomosaics(img, tile_size):
    img = cv.resize(img, (img.shape[1] - (img.shape[1] % tile_size), img.shape[0] - (img.shape[0] % tile_size)))

    for file_name in os.listdir(library_path):
        img_path = os.path.join(library_path, file_name)
        image = cv.imread(img_path)
        library[file_name] = cv.resize(image, (tile_size, tile_size))
    
    if not library:
        print("Error: Image library is empty.")
        exit()
    
    for file_name in library:
        cache[file_name] = np.mean(library[file_name], axis=(0, 1)).astype(int)
    
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