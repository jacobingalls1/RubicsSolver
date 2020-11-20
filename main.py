import numpy as np
import sys
import cv2
from faceMap import setFaces 
from rubik_solver import utils

images = []
videos = []

for i in sys.argv[1:]:
    if i.split[1] in ['mp4']:
        videos.append(i)
    else:
        images.append(i)

# colors are ints 0-5, these correspond to Yellow, Red, Green, Orange, Blue, and White

class Cube:
    def __init__(self):
        print("TODO: Cube()")
        self.faces = 0
        self.notatedList = [-1 for i in range(54)]
        
    def solution(self):
        print("TODO: Cube.solution()")

    def addFace(self, facesData): #faces are a 3x3 list of ints
        self.faces += faceMap(self.notatedList, facesData)

    def completeCube(self):
        return self.faces == 6
        print("TODO: Cube.completeCube()")


cube = Cube()

images = [cv2.imread(i) for i in images]

print("TODO: process images")

if cube.completeCube():
    print(cube.solution())
    exit()

for v in videos:
    print("TODO: process videos")

if cube.completeCube():
    print(cube.solution())
    exit()

print("Sorry, not enough information")



