#Finds color of image at a point and surround points
import cv2
import numpy as np



colors =[[[15,130,130], [40,255,255]], #y [0][0] was 20
         [[100,70,50], [120,255,255]], #B [0][1] was 130 [0][2] was 130
         [[30,60,60], [100,255,255]], #G [0][0] was 60 [0][1] was 100 [0][2] was 100
         [[5,130,130], [15,255,255]], #O [1][0] was 20
         [[0,20,120], [180,100,255]], #W [0][2] was 200
         [[150,130,130], [180,255,255]], #R1
         [[0,130,115], [10,255,255]]] #R2 [0][2] was 130


#Pass in image object, and point as a list
#Returns color with hsv values
def findColor(imageRGB, point):
    cv2.imshow("RGB", imageRGB)
    image = cv2.cvtColor(imageRGB, cv2.COLOR_BGR2HSV)
    #cv2.imshow("HSV", image) 

    #Find surrounding pixels
    bCount = 0
    gCount = 0
    rCount = 0
    for i in range(5):
        for j in range(5):
            b, g, r = image[int(point[0]) + i - 2, int(point[1]) + j - 2]
            bCount += b
            gCount += g
            rCount += r

    pointColor = [bCount/25, gCount/25, rCount/25]

    print(pointColor)


    imageRBG = cv2.rectangle(imageRGB, (point[1] - 2, point[0] - 2),(point[1] + 2, point[0] + 2), (255, 0, 0), 1)
    cv2.imshow("RGB", imageRGB)



    #Find color Name
    colorName = "No color identified"
    for i in range (7):
        color = colors[i]
        #print(color)
        if color[0][0] > pointColor[0] or color [1][0] < pointColor[0]:
            continue
        if color[0][1] > pointColor[1] or color [1][1] < pointColor[1]:
            continue
        if color[0][2] > pointColor[2] or color [1][2] < pointColor[2]:
            continue

        if 0<=i<=6:
            colorName = ['yellow', 'blue', 'green', 'orange', 'white', 'red', 'red'][i]
        else:
            colorName = "No color identified"
            
        
            
                
    #color = image[point[0],point[1]]

    return colorName


    

image = cv2.imread("testing/L0.jpg")
point = [220, 290]

print(findColor(image, point))
