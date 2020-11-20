import numpy as np
import cv2


def processImage(image):
    lowThresholds = [150, 60, 60]
    highThresholds = [200, 255, 255]
    
    height = image.shape[0]
    width = image.shape[1]

    #Convert to HSV
    hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    #Split into bands
    planes = cv2.split(hsvImage)


    #Output threshold image
    thresh_img = np.full((height, width), 255, dtype=np.uint8)
    for i in range (3):
        low_val = lowThresholds[i]
        high_val = highThresholds[i]

        NA,low_img = cv2.threshold(planes[i], low_val, 255, cv2.THRESH_BINARY)
        NA,high_img = cv2.threshold(planes[i], high_val, 255, cv2.THRESH_BINARY_INV)

        thresh_band_img = cv2.bitwise_and(high_img, low_img)


        thresh_img = cv2.bitwise_and(thresh_img, thresh_band_img)

    cv2.imshow("Thresholded image", thresh_img)
    cv2.waitKey(0)



myImage = cv2.imread("testing/s2wr.jpg")
myImage = cv2.resize(myImage, (500, 500))
processImage(myImage)
