# Author: Ruidi Huang
# CSCI437 Lab6


import cv2
import math
from statistics import stdev
from classes import Sticker
from colorAtPoint import findColor

center = [3, 17, 19]

faces = [[], [], []]


def distance_mag(pt1, pt2):
    dx = pt1[0] - pt2[0]
    dy = pt1[1] - pt2[1]
    magnitude = pow(pow(dx, 2) + pow(dy, 2), 0.5)
    return magnitude


def center_check(pts, center):
    sum = [0, 0]
    for i in range(len(pts)):
        sum[0] += pts[i][0]
        sum[1] += pts[i][1]
    sum[0] /= 8
    sum[1] /= 8

    dif = (abs(sum[0] - center[0]), abs(sum[1] - center[1]))
    if dif[0] < 20 and dif[1] < 20:
        return True
    else:
        return False


def find_center(pts, center, current_centroid, bgr_img):
    if center_check(pts, center) == False:
        return False

    dict = []

    for i in range(len(pts)):
        slope = abs(float(pts[i][1] - center[1]) / float(pts[i][0] - center[0]))
        true_slope = float(pts[i][1] - center[1]) / float(pts[i][0] - center[0])
        if slope > 3.0:
            slope = 3.0
            true_slope = 3.0
        elif slope < 0.05:
            slope = 0.001
            true_slope = 0.001
        dict.append([i, slope, true_slope])
        #if current_centroid == 9 and len(faces[0]) > 0 :
        # if current_centroid == 4 and len(faces[0]) == 0:
        #     print(float(pts[i][1] - center[1]) / float(pts[i][0] - center[0]))
        #     center_check(pts, center)
        #     cv2.line(bgr_img, (int(pts[i][0]), int(pts[i][1])), (int(center[0]), int(center[1])), color=(0,0,0), thickness=2)
        #     cv2.imshow("lines", bgr_img)
        #     cv2.waitKey(0)

    while (len(dict) > 1):
        for i in range(1, len(dict)):
            pt1 = dict[0]
            pt2 = dict[i]

            if abs(dict[i][1] - dict[0][1]) <= 0.32:
                if dict[i][2]/dict[0][2] > 0 :
                    dict.remove(pt1)
                    dict.remove(pt2)
                    # if current_centroid == 4 and len(faces[0]) == 0:
                    #     print(dict)
                    break
            if i == len(dict) - 1:

                return False

    if not dict:
        return True
    else:

        return False


def sort_distance_index(distances, index):
    dis = distances
    ind = index
    for i in range(len(dis)):
        for j in range(len(dis)):
            if dis[i] < dis[j]:
                tmp_i = ind[i]
                ind[i] = ind[j]
                ind[j] = tmp_i

                tmp_d = dis[i]
                dis[i] = dis[j]
                dis[j] = tmp_d

    return dis, ind


def center_filter(imageWidth, imageHeight, whiteCentroids, blackCentroids, bgr_img):
    dis_to_center_black = []
    center = (imageWidth / 2, imageHeight / 2)

    # Calculate the distance of the black centroids with proper area to the center of the image
    for i in range(len(blackCentroids)):
        dx = blackCentroids[i][0] - center[0]
        dy = blackCentroids[i][1] - center[1]
        dis_to_center_black.append(pow(pow(dx, 2) + pow(dy, 2), 0.5))

    # find the one closest to the center
    min_val = min(dis_to_center_black)
    min_index = -1
    for i in range(len(dis_to_center_black)):
        if dis_to_center_black[i] == min_val:
            min_index = i
            break

    # eliminate all points outside of the circle
    # cube_center = (int(blackCentroids[min_index][0]), int(blackCentroids[min_index][1]))
    cube_center = (int(imageHeight / 2), int(imageWidth / 2))
    radius = 180
    # radius = pow(blackCentroids[min_index][2] / (math.pi), 0.5)
    # radius = radius * 1.5
    # cv2.circle(bgr_img, center=cube_center, radius=int(radius), color=(255, 0, 0),thickness=-1)
    # cv2.imshow("Area of interest", bgr_img)
    # cv2.waitKey(0)
    white_centroids = []
    for i in range(len(whiteCentroids)):
        dx = whiteCentroids[i][0] - cube_center[0]
        dy = whiteCentroids[i][1] - cube_center[1]

        dis_to_cube = pow(pow(dx, 2) + pow(dy, 2), 0.5)
        if (dis_to_cube <= radius):
            white_centroids.append(whiteCentroids[i])

    return white_centroids


def closest_pt(args):
    pass


def find_sides(image=cv2.imread("testing/L1.jpg"), demo=False):
    # Read image
    imW = 480
    bgr_img = image
    bgr_img = cv2.resize(bgr_img, (int(imW), int(imW * bgr_img.shape[0] / bgr_img.shape[1])))

    bgr_img_backup = cv2.resize(bgr_img, (int(imW), int(imW * bgr_img.shape[0] / bgr_img.shape[1])))
    image_height = bgr_img.shape[0]
    image_width = bgr_img.shape[1]

    gray_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)

    binary_img = cv2.adaptiveThreshold(src=gray_img, maxValue=255, adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C,
                                       thresholdType=cv2.THRESH_BINARY, blockSize=31, C=15)

    # Clean up using opening + closing.
    ksize = 2
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ksize, ksize))
    binary_img = cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, kernel)
    ksize = 1
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ksize, ksize))
    binary_img = cv2.morphologyEx(binary_img, cv2.MORPH_CLOSE, kernel)

    if demo:
        cv2.imshow("binary", binary_img)
        cv2.waitKey(0)

    # Find connected components
    num_labels, labels_img, stats, centroids = cv2.connectedComponentsWithStats(binary_img)

    centroid_threshold = 0.8
    centroid_location_white = []
    centroid_location_black = []

    # Find white centroids
    for n in range(num_labels):
        xc, yc = centroids[n]
        area = stats[n, cv2.CC_STAT_AREA]
        if area > 150 and area < 10000:  # was 50 and 8000 for L1
            centroid_location_white.append((xc, yc, area))

    # reverse black and white and find Black centroids
    binary_img = cv2.bitwise_not(binary_img)
    if demo:
        cv2.imshow("reverse_binary", binary_img)
        cv2.waitKey(0)
    num_labels, labels_img, stats, centroids = cv2.connectedComponentsWithStats(binary_img)

    # Find black centroids
    for n in range(num_labels):
        xc, yc = centroids[n]
        area = stats[n, cv2.CC_STAT_AREA]
        if 8000 < area:
            centroid_location_black.append((xc, yc, area))

    # filter out outliers
    centroid_location_white = center_filter(binary_img.shape[0], binary_img.shape[1], centroid_location_white,
                                            centroid_location_black, bgr_img);

    # draw points
    for i in range(len(centroid_location_white)):
        cv2.circle(bgr_img, center=(int(centroid_location_white[i][0]), int(centroid_location_white[i][1])), radius=5,
                   color=(0, 0, 255), thickness=-1)
        # cv2.putText(bgr_img, text=str(i),
        #             org=(int(centroid_location_white[i][0]), int(centroid_location_white[i][1])),
        #             fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 0, 0))

    cv2.imshow("centroids", bgr_img)
    cv2.waitKey(0)

    i = 3
    while len(centroid_location_white) > 0:
        if i == len(centroid_location_white) - 1:
            print("No face found")
            break
        distance = []
        index = []
        for j in range(len(centroid_location_white)):
            if i != j:
                dx = centroid_location_white[i][0] - centroid_location_white[j][0]
                dy = centroid_location_white[i][1] - centroid_location_white[j][1]
                distance.append(pow(pow(dx, 2) + pow(dy, 2), 0.5))
                index.append(j)

        distance, index = sort_distance_index(distance, index)

        left = []
        right = []
        vertical_pts = []
        closest_pts = []
        start_pt = (centroid_location_white[i][0], centroid_location_white[i][1], centroid_location_white[i][2])

        # if (len(faces[0]) > 0):
        #     print(i)
        #     cv2.circle(bgr_img, (int(start_pt[0]),int(start_pt[1])), radius=5, color=(0,0,0), thickness=-1)
        #     cv2.imshow("start", bgr_img)
        #     cv2.waitKey(0)
        for z in range(len(distance)):
            indx = index[z]
            dx = centroid_location_white[indx][0] - start_pt[0]

            if len(left) + len(right) + len(vertical_pts) == 8:
                break

            if abs(dx) < 6 and len(vertical_pts) < 2:
                vertical_pts.append(centroid_location_white[indx])
                continue

            if (centroid_location_white[indx][0] < start_pt[0]):
                if len(left) < 3:
                    left.append(centroid_location_white[indx])
            elif (centroid_location_white[indx][0] > start_pt[0]):
                if len(right) < 3:
                    right.append(centroid_location_white[indx])

        # cv2.circle(bgr_img, (int(start_pt[0]), int(start_pt[1])), radius=5, color=(0, 0, 0), thickness=-1)
        # cv2.imshow("start", bgr_img)
        # cv2.waitKey(0)

        # if (i == 8) and len(faces[0]) > 0:
        #     print(start_pt)

        for l in left:
            closest_pts.append(l)
            # if (i == 8) and len(faces[0]) > 0:
            #     print(l)
            #     cv2.circle(bgr_img, (int(l[0]), int(l[1])), radius=5, color=(0, 0, 0), thickness=-1)
            #     cv2.imshow("left", bgr_img)
            #     cv2.waitKey(0)
        for r in right:
            closest_pts.append(r)
            # if (i == 8) and len(faces[0]) > 0:
            #     print(r)
            #     cv2.circle(bgr_img, (int(r[0]), int(r[1])), radius=5, color=(255, 255, 255), thickness=-1)
            #     cv2.imshow("right", bgr_img)
            #     cv2.waitKey(0)
        for v in vertical_pts:
            closest_pts.append(v)

        # if i == 4:
        #     print(len(vertical_pts))
        #     print(len(closest_pts))

        is_center = find_center(closest_pts, start_pt, i, bgr_img)
        if is_center:  # add the pts to faces if a center of a face is found
            temp = []
            for pt in closest_pts:
                temp.append((pt[0], pt[1]))
            # temp = closest_pts
            temp.append((start_pt[0], start_pt[1]))

            for p in range(len(faces)):
                if len(faces[p]) == 0:
                    faces[p] = temp
                    # draw the points base on the face
                    color = (0, 0, 0)
                    if p == 0:
                        color = (255, 0, 0)
                    elif p == 1:
                        color = (0, 255, 0)
                    elif p == 2:
                        color = (0, 0, 255)
                    for q in range(len(closest_pts)):
                        if demo:
                            cv2.circle(bgr_img, center=(int(faces[p][q][0]), int(faces[p][q][1])), radius=5,
                                       color=color, thickness=-1)
                        centroid_location_white.remove(closest_pts[q])
                    centroid_location_white.remove(start_pt)
                    # if p == 1:
                    #     color = (0, 0, 0)
                    cv2.circle(bgr_img, center=(int(start_pt[0]), int(start_pt[1])), radius=5, color=color,
                               thickness=-1)

                    i = 0
                    break
        else:
            i += 1

    # for i in range(len(faces)):
    #     print(len(faces[i]))

    if demo:
        cv2.imshow("show faces on cube", bgr_img)
        cv2.waitKey(0)
        exit()

    # secaf = []
    # for i in range(len(faces)):
    #     temp = []
    #     for j in range(len(faces[i])):
    #         temp.append((faces[i][j][1], faces[i][j][0]))
    #     secaf.append(temp)


    for f in range(len(faces)):
        faces[f] = [Sticker(findColor(bgr_img_backup, i), i) for i in faces[f]]

    return faces


find_sides(image=cv2.imread("testing/L3.jpg"), demo=True)
