import cv2
import numpy as np

max_dist = 50
triallowance = 3 #units away from midpoint of third point
# x = allowance/sqrt(1+slope**2)

def clockwise(p):
    s = 0
    for i in range(len(p)):
        s += (p[i][0] - p[i-1][0])*(p[i][1]+p[i-1][1])
    return s > 0

def inTriangle(test, a, b, c): #working as intended
    curr = clockwise([test, a, b])
    return not(clockwise([test, b, c]) == curr and clockwise([test, c, a]) == curr)

def isLine(a, b, c): #where c is the midpoint
    mid = ((a[0]+b[0])/2, (a[1]+b[1])/2)
    perpslope = (b[1]-a[1])/(b[0]-a[0]+.00001) #saves a multiply, like it'll help
    x = triallowance/np.sqrt(1+perpslope**2)
    p1, p2 = (mid[0]+x, mid[1]+perpslope*x), (mid[0]-x, mid[1]-perpslope*x)
    print(a, b, p1, p2)
    print(inTriangle(p1, a, b, c))
    return inTriangle(p1, a, b, c) or inTriangle(p2, a, b, c)


#colinear triplets according to whether the middle point is within a triangle formed by the others and an allowance
def get_lines(centroids):
    a, b, c = [0,0], [100,100], [52, 52]
    print(isLine(a, b, c))
    return []
    true, false = 0,0
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

