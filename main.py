import numpy as np
import sys
import cv2
import faceMap
import time
from classes import Cube, Sticker
from imageProcess import get_faces
from centroidProcess import format_faces
from faceMap import setFaces 
from rubik_solver import utils


images = []
videos = []

imW = 480

for i in sys.argv[1:]:
    if i.split('.')[-1] in ['mp4']:
        videos.append(i)
    else:
        images.append(i)

cube = Cube()

def perFrame(image):
    image = cv2.resize(image, (int(imW), int(imW*image.shape[0]/image.shape[1])))
    faces = get_faces(image)
    for i in faces:
        cube.setFaces(i)
        cube.cubeSolve()
    cv2.imwrite("output.png", image)


for im in images:
    t0 = time.time_ns() 
    image = cv2.imread(im)
    perFrame(image)
    print("took %f seconds" %((time.time_ns()-t0)/100000000))

cube.cubeSolve()

for v in videos:
    print("TODO: process videos")

cube.cubeSolve()

print("Sorry, not enough information")



