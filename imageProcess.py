import cv2
import numpy as np

max_dist = 50
areaLo = 300
areaHi = 5000


#YBRGOW
colors = [[np.matrix([0,130,130]),np.matrix([30,255,255])], #Y
          [np.matrix([100,130,130]),np.matrix([120,255,255])], #B
          [np.matrix([150,130,130]),np.matrix([180,255,255])], #R1
          [np.matrix([60,100,100]),np.matrix([100,255,255])], #G
          [np.matrix([5,130,130]),np.matrix([20,255,255])], #O
          [np.matrix([0,20,200]),np.matrix([180,100,255])], #W
          [np.matrix([0,130,130]),np.matrix([10,255,255])]] #R2


def distance(a, b):
    return (a[0]-b[0])**2 + (a[1]-b[1])**2

def get_lines(centroids):
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

def get_centroids(image):
    imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    centroids = [[] for i in range(len(colors)-1)]

    for c in range(len(colors)-1):
        mask = cv2.inRange(imageHSV, colors[c][0], colors[c][1])
        mskimg = cv2.bitwise_and(imageHSV, imageHSV, mask=mask)
        if c == 2:
            mask = cv2.inRange(imageHSV, colors[-1][0], colors[-1][1])
            mskimg2 = cv2.bitwise_and(imageHSV, imageHSV, mask=mask)
            mskimg += mskimg2
        im = cv2.cvtColor(mskimg, cv2.COLOR_HSV2BGR)
        gim = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        _,gim = cv2.threshold(gim, 1, 255, cv2.THRESH_BINARY)
        kernel = np.ones((6,6), np.uint8)
        gim = cv2.morphologyEx(gim, cv2.MORPH_OPEN, kernel, iterations = 2)
        retval, labels, stats, cent = cv2.connectedComponentsWithStats(gim, 4, cv2.CV_32S)

        cv2.imwrite(f"{c}.png", gim)
        print(cent)
        for i in range(len(stats)):
            if c == 0:
                print(stats[i, cv2.CC_STAT_AREA])
            if areaLo < stats[i, cv2.CC_STAT_AREA] < areaHi:
                centroids[c].append(cent[i])

    return centroids


get_centroids(cv2.imread('./testing/'))
