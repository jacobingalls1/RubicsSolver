import numpy as np
import sys
import cv2

images = []
videos = []

for i in sys.argv[1:]:
    if i.split[1] in ['mp4']:
        videos.append(i)
    else:
        images.append(i)

class Cube:
    def __init__():
        print("TODO: Cube()")
        faces = {}

    def solution():
        print("TODO: Cube.solution()")

    def completeCube():
        return len(faces.keys) == 6
        print("TODO: Cube.completeCube()")


cube = Cube()

images = [cv2.imread(i) for i in images]

print("TODO: process images")

if cube.completeCube():
    print cube.solution()
    exit()

for v in videos:
    print("TODO: process videos")

if cube.completeCube():
    print cube.solution()
    exit()

print("Sorry, not enough information")



