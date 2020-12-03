import cv2
import numpy as np

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


