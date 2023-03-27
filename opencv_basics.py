import cv2 as cv
import numpy as np

img1 = cv.imread('100.jpg')
img2 = cv.imread('400.jpg')
img3 = cv.imread('418.jpg')
img4 = cv.imread('102.jpg')

# Resize all images to the same size
img1 = cv.resize(img1, (300, 300))
img2 = cv.resize(img2, (300, 300))
img3 = cv.resize(img3, (300, 300))
img4 = cv.resize(img4, (300, 300))

alpha = 1.2
beta = -30

border_size = 10
border_color = (255, 255, 255)

# Rotate the images
M1 = cv.getRotationMatrix2D((150, 150), 45, 1.0)
M2 = cv.getRotationMatrix2D((150, 150), 315, 1.0)
M3 = cv.getRotationMatrix2D((150, 150), 135, 1.0)
M4 = cv.getRotationMatrix2D((150, 150), 225, 1.0)
img1 = cv.warpAffine(img1, M1, (300, 300))
img2 = cv.warpAffine(img2, M2, (300, 300))
img3 = cv.warpAffine(img3, M3, (300, 300))
img4 = cv.warpAffine(img4, M4, (300, 300))

# Add a pinkish tint to the shadows and highlights
img1[:,:,0] += 30
img1[:,:,1] += 5
img1[:,:,2] -= 20
img2[:,:,0] += 30
img2[:,:,1] += 5
img2[:,:,2] -= 20
img3[:,:,0] += 30
img3[:,:,1] += 5
img3[:,:,2] -= 20
img4[:,:,0] += 30
img4[:,:,1] += 5
img4[:,:,2] -= 20

# Increase overall brightness and contrast
img1 = cv.convertScaleAbs(img1, alpha=alpha, beta=beta)
img2 = cv.convertScaleAbs(img2, alpha=alpha, beta=beta)
img3 = cv.convertScaleAbs(img3, alpha=alpha, beta=beta)
img4 = cv.convertScaleAbs(img4, alpha=alpha, beta=beta)

# Increase saturation
hsv1 = cv.cvtColor(img1, cv.COLOR_BGR2HSV)
hsv1[:,:,1] += 30
img1 = cv.cvtColor(hsv1, cv.COLOR_HSV2BGR)
hsv2 = cv.cvtColor(img2, cv.COLOR_BGR2HSV)
hsv2[:,:,1] += 30
img2 = cv.cvtColor(hsv2, cv.COLOR_HSV2BGR)
hsv3 = cv.cvtColor(img3, cv.COLOR_BGR2HSV)
hsv3[:,:,1] += 30
img3 = cv.cvtColor(hsv3, cv.COLOR_HSV2BGR)
hsv4 = cv.cvtColor(img4, cv.COLOR_BGR2HSV)
hsv4[:,:,1] += 30
img4 = cv.cvtColor(hsv4, cv.COLOR_HSV2BGR)

# Add borders to images
img1 = cv.copyMakeBorder(img1, 0, border_size, 0, border_size, cv.BORDER_CONSTANT, value=border_color)
img2 = cv.copyMakeBorder(img2, 0, border_size, border_size, 0, cv.BORDER_CONSTANT, value=border_color)
img3 = cv.copyMakeBorder(img3, border_size, 0, 0, border_size, cv.BORDER_CONSTANT, value=border_color)
img4 = cv.copyMakeBorder(img4, border_size, 0, border_size, 0, cv.BORDER_CONSTANT, value=border_color)

# Create collage
top_row = cv.hconcat([img1, img2])
bottom_row = cv.hconcat([img3, img4])
collage = cv.vconcat([top_row, bottom_row])

# Display the collage
cv.imshow('Filtered Image', collage)
cv.waitKey(0)
cv.destroyAllWindows()