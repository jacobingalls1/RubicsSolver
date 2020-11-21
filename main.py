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

# colors are chars, 'O', 'B', 'R', 'W', 'Y', 'G'

class Cube:
    def __init__(self):
        self.faces = 0
        self.notatedList = ['-' for i in range(54)]
        
    def solution(self):
        print("TODO: Cube.solution()")

# faces are a 3x3 list of ints, facesData will be two of these,
# joined so that the final column of the first is adjacent to 
# the first column of the last
    def addFace(self, facesData): 
        self.faces += faceMap(self.notatedList, facesData)

    def completeCube(self):
        return self.faces == 6

    def printCube(self): #could be improved to cube net
        print()
        counter = 0
        for i in range(6):
            for j in range(9):
                print(self.notatedList[counter], end='')
                counter += 1
            print()
        print()
        

cube = Cube()

cube.printCube()

input1 = 'groryrgrg'
input2 = 'bbbwbgooo'

input3 = 'ooorrrrrr'
input4 = 'bbbgggggg'

input5 = 'oorooroor'
input6 = 'wwwwwwwww'

inputs = [input1, input2, input3, input4, input5, input6]

f1 = [[0 for j in range(3)] for i in range(3)]
f2 = [[0 for j in range(3)] for i in range(3)]
f3 = [[0 for j in range(3)] for i in range(3)]
f4 = [[0 for j in range(3)] for i in range(3)]
f5 = [[0 for j in range(3)] for i in range(3)]
f6 = [[0 for j in range(3)] for i in range(3)]

faces = [f1,f2,f3,f4,f5,f6]

count = -1
for i in range(3):
    for j in range(3):
        count += 1
        for f in range(len(faces)):
            faces[f][i][j] = inputs[f][count].upper()



setFaces(cube.notatedList, [f1,f2])
setFaces(cube.notatedList, [f3,f4])
setFaces(cube.notatedList, [f5,f6])

cube.printCube()

exit()
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



