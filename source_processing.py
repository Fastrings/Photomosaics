import os
import cv2 as cv
import numpy as np

src_dir = "./Source_Images"
dst_dir = "./Cropped_Images"


def crop(img):
    for filename in os.listdir(src_dir):
        if filename.endswith(".jpg"):
            full_path = os.path.join(src_dir, filename)
            img = cv.imread(full_path)
            size = min(img.shape)
            cropped = img[0:size, 0:size]
            full_dst_path = os.path.join(dst_dir, filename)
            cv.imwrite(full_dst_path, cropped)