import numpy as np
import cv2


def processImage(image, col):
    lowThresholds = [0, 60, 60]
    highThresholds = [255, 255, 255]
    
    height = image.shape[0]
    width = image.shape[1]

    #Convert to HSV
    hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    #Split into bands
    if col in ['r', 'g', 'b', 'y', 'w']:
        planes = cv2.split(image)
        lowThresholds = [100, 100, 100]
        highThresholds = [255, 255, 255]
    elif col == 'o':
        planes = cv2.split(hsvImage)
        lowThresholds = [0, 100, 100]
        highThresholds = [50, 255, 255]

    yes, no = getColorPlane(col)

    #Output threshold image
    thresh_img = np.full((height, width), 255, dtype=np.uint8)
    for i in yes:
        low_val = lowThresholds[i]
        high_val = highThresholds[i]

        NA,low_img = cv2.threshold(planes[i], low_val, 255, cv2.THRESH_BINARY)
        NA,high_img = cv2.threshold(planes[i], high_val, 255, cv2.THRESH_BINARY_INV)

        thresh_band_img = cv2.bitwise_and(high_img, low_img)

        thresh_img = cv2.bitwise_and(thresh_img, thresh_band_img)

    thresh_img2 = np.full((height, width), 255, dtype=np.uint8)
    for i in no:
        low_val = lowThresholds[i]
        high_val = highThresholds[i]

        NA,low_img = cv2.threshold(planes[i], low_val, 255, cv2.THRESH_BINARY)
        NA,high_img = cv2.threshold(planes[i], high_val, 255, cv2.THRESH_BINARY_INV)

        thresh_band_img = cv2.bitwise_and(high_img, low_img)

        thresh_img2 = cv2.bitwise_xor(thresh_img2, thresh_band_img)

    thresh_img = cv2.bitwise_and(thresh_img, thresh_img2)

    return thresh_img


def getColorPlane(col):
    if col == 'r':
        return ([2], [0, 1])
    if col == 'b':
        return ([0], [1, 2])
    if col == 'g':
        return ([1], [0, 2])
    if col == 'y':
        return ([1, 2], [0])
    if col == 'o':
        return ([0, 1, 2], [])
    if col == 'w':
        return ([0, 1, 2], [])
    else:
        return []


def processAllColors(image):
    processed = {}
    for c in ['w', 'r', 'g', 'b', 'y', 'o']:
        if c == 'w':
            processed[c] = processImage(image, c)
        else:
            processed[c] = cv2.bitwise_and(processImage(image, c), cv2.bitwise_not(processed['w']))
            if c == 'o':
                processed[c] = cv2.bitwise_and(processImage(image, c), cv2.bitwise_not(processed['y']))
    return processed
