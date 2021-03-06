import cv2
import numpy as np
from collections import defaultdict
import math

def dist(a, b):
    return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

def closest(target, poss):
    
    return min([p for p in poss if p.piece == 'e'], key=lambda p: dist(target, p.pos))

def rotate(face, rot):
    for i in range(rot):
        face = [face[6], face[3], face[0], face[7], face[4], face[1], face[8], face[5], face[2]]
    return [face[0].color[0]+face[1].color[0]+face[2].color[0],
            face[3].color[0]+face[4].color[0]+face[5].color[0],
            face[6].color[0]+face[7].color[0]+face[8].color[0]]


#faces is a list of lists with at 9 stickers - colors and positions, left to right, top to bottom
def format_faces(faces):
    for f in range(len(faces)):
        faces[f] = faces[f][0]+faces[f][1]+faces[f][2]
        print(faces[f])
    facePairs =  []
    toFormat = [[faces[0], faces[1]]]
    if len(faces) == 3:
        toFormat.append([faces[1],faces[2]])
    for f in toFormat:
        print("two faced")
        [print(fa, '\n') for fa in f]
        c1 = f[0][4].pos
        c2 = f[1][4].pos
        cl1 = closest(c2, f[0])
        re1 = f[0].index(cl1)
        print(re1)
        #rotations are clockwise
        rot1 = [None, 1, None, 2, None, 0, None, 3][re1]
        le2 = f[1].index(closest(c1, f[1]))
        print(le2)
        rot2 = [None, 3, None, 0, None, 2, None, 1][le2]
        f1 = rotate(f[0].copy(), rot1)
        f2 = rotate(f[1].copy(), rot2)
        facePairs.append([f1,f2])
    return facePairs


'''
def clockwise(p):
    s = 0
    for i in range(len(p)):
        s += (p[i][0] - p[i-1][0])*(p[i][1]+p[i-1][1])
    return s > 0

def inTriangle(test, a, b, c): #working as intended
    curr = clockwise([test, a, b])
    return clockwise([test, b, c]) == curr and clockwise([test, c, a]) == curr

def isLine(a, b, c): #where c is the midpoint
    mid = ((a[0]+b[0])/2, (a[1]+b[1])/2)
    perpslope = (b[1]-a[1])/(b[0]-a[0]+.00001) #saves a multiply, like it'll help
    x = triallowance/np.sqrt(1+perpslope**2)
    p1, p2 = (mid[0]+x, mid[1]+perpslope*x), (mid[0]-x, mid[1]-perpslope*x)
    #print(a, b, p1, p2)
    return inTriangle(c, a, b, p1) or inTriangle(c, a, b, p2)


#colinear triplets according to whether the middle point is within a triangle formed by the others and an allowance
def get_lines(centroids):
    #a, b, c = [0,0], [100,100], [52, 52]
    true, false = 0,0
    taken = defaultdict(lambda: defaultdict(lambda: []))
    lines = []
    for ip in range(len(centroids)):
        i = centroids[ip]
        for jp in range(ip, len(centroids)):
            if ip==jp:
                continue
            j = centroids[jp]
            for k in range(len(centroids)):
                if k==jp or k==ip or k in taken[ip][jp]:
                    print(ip, jp, k)
                    continue
                taken[ip][jp].append(k)
                if isLine(i, j, centroids[k]):
                    lines.append((ip, jp, k))
                    true += 1
                else:
                    false += 1
    print(true, false)
    return lines

#return all colinear triplets of centroids as judged by two ends and a midpoint
def get_lines_old(centroids):
    lines = []
    for ip in range(len(centroids)):
        i = centroids[ip]
        for jp in range(len(centroids)):
            if ip==jp:
                continue
            j = centroids[jp]
            p = (i+j)/2
            for k in range(len(centroids)):
                if k==jp or k==ip:
                    continue
                if distance(p, centroids[k]) < max_dist:
                    lines.append((i, j))
    return lines

#return 3 lists: centers, edges, and corners
def get_pieces(lines):
    ret = [[],[],[]]
'''
