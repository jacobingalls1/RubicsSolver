import numpy as np
import sys
import cv2
import faceMap
import time
from classes import Cube, Sticker
from find_cube_side import find_sides
from orderStickers import order
from makeRows import make_rows
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

images.append('./testing/L2.jpg')
images.append('./testing/L3.jpg')

cube = Cube()

def stickerPos(sticker):
    return (int(sticker.pos[0]), int(sticker.pos[1]))

def perFrame(image):
    image = cv2.resize(image, (int(imW), int(imW*image.shape[0]/image.shape[1])))
    faces = find_sides(image)
    faces = [i for i in faces if i!=[]]
    if len(faces) < 2:
        return
    for ip in range(len(faces)):
        i = faces[ip]
        print("ordering")
        border = order(i.copy())
        for j in i:
            color = (255,0,0)
            if j.piece == 'e':
                color = (0,255,0)
            if j.piece == 'r':
                color = (0,0,255)
            cv2.circle(image, stickerPos(j), 3, color, -1)
        cv2.imwrite("output.png", image)
        faces[ip] = make_rows(i, border)

    facePairs = format_faces(faces)
    for j in facePairs:
        cube.addFace(j)
    cube.solve()
    cv2.imwrite("output.png", image)

for im in images:
    t0 = time.time_ns() 
    image = cv2.imread(im)
    perFrame(image)
    print("took %f seconds" %((time.time_ns()-t0)/100000000))


for v in videos:
    print("TODO: process videos")


print("Sorry, not enough information")



