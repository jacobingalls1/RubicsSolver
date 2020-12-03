import numpy as np
import sys
import cv2
import faceMap
from faceMap import setFaces 
from imageProcess import get_centroids, get_lines 
from rubik_solver import utils


images = []
videos = []

imW = 480

for i in sys.argv[1:]:
    if i.split('.')[-1] in ['mp4']:
        videos.append(i)
    else:
        images.append(i)

# colors are chars, 'Y', 'B', 'R', 'G', 'O', 'W'

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
        return self.notatedList.count('-') == 0

    def printCube(self): #could be improved to cube net
        print()
        counter = 0
        for i in range(6):
            for j in range(9):
                print(self.notatedList[counter], end='')
                counter += 1
            print()
        print()

    def solve(self):
        if not self.completeCube():
            print("Cube is not yet complete! Cannot solve.")
            return
        print(utils.solve(''.join(self.notatedList), 'Kociemba'))
        

cube = Cube()


'''
f1 = [[0 for j in range(3)] for i in range(3)]
f2 = [[0 for j in range(3)] for i in range(3)]
f3 = [[0 for j in range(3)] for i in range(3)]
f4 = [[0 for j in range(3)] for i in range(3)]
f5 = [[0 for j in range(3)] for i in range(3)]
f6 = [[0 for j in range(3)] for i in range(3)]

input1 = 'ywboowwry'
input2 = 'yryoybogw'

input3 = 'rgwrgyobr'
input4 = 'owwrrybyr'

input5 = 'gbrywwgbo'
input6 = 'bgggbobog'

inputs = [input1, input2, input3, input4, input5, input6]
faces = [f1,f2,f3,f4,f5,f6]

count = -1
for i in range(3):
    for j in range(3):
        count += 1
        for f in range(len(faces)):
            faces[f][i][j] = inputs[f][count]

setFaces(cube.notatedList, [f1,f2])
setFaces(cube.notatedList, [f3,f4])
setFaces(cube.notatedList, [f5,f6])

cube.printCube()

cube.solve()
'''


for im in images:
    print(im)
    image = cv2.imread(im)
    image = cv2.resize(image, (int(imW), int(imW*image.shape[0]/image.shape[1])))
    cents = get_centroids(image)
    #centroids are mostly correct, some trouble with yellow and red
    combinedCents = []
    for i in cents[1:]:
        for j in i:
            combinedCents.append(j)
            cv2.circle(image, tuple(np.int32(j)), 5, (255,0,0))

    print(len(combinedCents))
    lines = get_lines(combinedCents)
    #lines looks about correct too, some problems involved in the shifting of midpoints over nonlinear transforms
    for i in lines:
        cv2.line(image, tuple(np.int32(i[0])), tuple(np.int32(i[1])), (0,0,255), 1)

    cv2.imwrite("output.png", image)


if cube.completeCube():
    print(cube.solution())
    exit()

for v in videos:
    print("TODO: process videos")

if cube.completeCube():
    print(cube.solution())
    exit()

print("Sorry, not enough information")



