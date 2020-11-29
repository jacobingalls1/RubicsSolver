import cv2
import numpy as np
from ProcessImage import processAllColors


MIN_FRACT_EDGES = 0.05  # prob between 0.05 and 0.08
MAX_FRACT_EDGES = 0.08

MIN_HOUGH_VOTES_FRACTION = 0.03
MIN_LINE_LENGTH_FRACTION = 0.05


def detectSquares(img):
    binaries = processAllColors(img)
    detPts = {}
    for k, v in binaries.items():
        detPts[k] = findSquares(v)



def findSquares(image):
    img = cv2.bitwise_not(image)
    height, width = img.shape
    ret1, ret2, ret3 = cv2.findContours(
        img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )
    cont = []
    for c in ret2:
        x,y,w,h = cv2.boundingRect(c)
        if w > 30 and h > 30:
            cont.append((x,y))
    return cont


img = cv2.imread('testing/c2gy.jpg')
img = cv2.resize(img, (500, 500))
detectSquares(img)
