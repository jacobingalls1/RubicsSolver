from faceMap import setFaces
#colors are chars: y b r g o w
class Sticker:
    def __init__(self, color='-', pos=(0,0)):
        self.color = color
        self.pos = pos
        self.dist = {}
        self.piece = '-'

    def __repr__(self):
        return " %s %s at (%i, %i)"%(self.piece, self.color, self.pos[0], self.pos[1])

    def __eq__(self, other):
        return self.pos[0] == other.pos[0] and self.pos[1] == other.pos[1]


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
        setFaces(self.notatedList, facesData)

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


