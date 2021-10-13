#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 16:20:15 2021

@author: angelobarona
"""

import numpy as np
import cv2
import time

def createMask(color, hsvImage):
    colorRange = {
            "red": [np.array([136, 87, 111], np.uint8), np.array([180, 255, 255], np.uint8)],
            "green": [np.array([25, 52, 72], np.uint8), np.array([102, 255, 255], np.uint8)],
            "blue": [np.array([94, 80, 2], np.uint8), np.array([130, 255, 255], np.uint8)] #[np.array([94, 80, 2], np.uint8), np.array([120, 255, 255], np.uint8)]
        }
    
    low, high = colorRange[color]
    
    return cv2.inRange(hsvImage, low, high)


def contourDefinition(andMask,kernel):
    dilation = cv2.dilate(andMask,kernel,iterations=3)
    #andMask = cv2.bitwise_and(hsvImg, hsvImg, mask = color)
    erosion = cv2.erode(dilation,kernel,iterations=3)
    smooth = cv2.GaussianBlur(erosion,(5,5),0)
    canny = cv2.Canny(smooth,100,200)
    contours,_ = cv2.findContours(np.array(canny),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    return contours


# def giveColorArray(color):
    
#     colorArray = {
#             "red": (0, 0, 255),
#             "green": (0, 255, 0),
#             "blue": (255, 0, 0)
#         }
    
#     return colorArray[color]


def identifying(contours, color, image):
        
    #colorA = giveColorArray(color)
    xWorld, yWorld = ['x','x']
    
    for i, contour in enumerate(contours):
        perimeter = 0.1 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, perimeter, True)
                
        if (len(approx) == 4 or len(approx) == 6):
            
            area = cv2.contourArea(contour)
            
            if(area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                ratio = w / float(h)
                                
                if ((0.8 <= ratio <= 1.20) or len(approx) == 6):
                    image = cv2.rectangle(image, (x, y), (x + w, y + h), (255,255,255), 2)
                  
                    #cv2.putText(image, color, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, colorA)
                    
                    xScreen, yScreen = objectCoords(contour)
                    
                    cv2.drawMarker(image,(xScreen,yScreen), color=(255,255,255), markerType=cv2.MARKER_STAR)
    
                    xWorld, yWorld = worldCoords(xScreen, yScreen, image)
                    worldString = str('%.3f'%xWorld) + ',' + str('%.3f'%yWorld)
                    
                    cv2.putText(image, worldString, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (30,255,255))
                    
                    #cv2.drawContours(img,contoursBlue,-1,(255,255,255),3)
    return xWorld, yWorld


def objectCoords(contour):
    
    moments = cv2.moments(contour)
                    
    xCenter = int(moments['m10']/moments['m00'])
    yCenter = int(moments['m01']/moments['m00'])
    
    return xCenter, yCenter


def worldCoords(xScreen, yScreen, image):
    
    xCenterOfProjection = 8.37012443e+02
    yCenterOfProjection = 4.95061830e+02
    xFocalPoint = 1.57323206e+03
    yFocalPoint = 1.55743567e+03
    zDistance = 0.3
    
    xWorld = (xScreen - xCenterOfProjection) * zDistance / xFocalPoint
    
    yWorld = (yScreen - yCenterOfProjection) * zDistance / yFocalPoint
    
    cv2.drawMarker(image,(int(xCenterOfProjection), int(yCenterOfProjection)), color=(0,0,0), markerType=cv2.MARKER_CROSS)
    
    return xWorld, yWorld

def confirmDetection(xCoordList, yCoordList):
    xCoordArray = np.asarray(xCoordList)
    yCoordArray = np.asarray(yCoordList)
    
    stdX = np.std(xCoordArray) 
    stdY = np.std(yCoordArray) 
    
    if stdX < 1 and stdY < 1:
        print (xCoordArray[-1], yCoordArray[-1])
        print(stdX,stdY)
        return True
    
    else:
        return False
    

def coordinateTransform(xWorld, yWorld):
    zWorld = 0.3
    cos = np.cos(-np.pi / 2)
    sin = np.sin(-np.pi / 2)
    l2_l3 = 0.315 + 0.045  # length from shoulder to base
    l10 = 0.12  # length from camera to shoulder
    
    coordsFromCamera = np.array([xWorld, yWorld, zWorld, 1])
    
    rotationMat1 = np.array([[1, 0, 0, 0],
                             [0, cos, -sin, 0],
                             [0, sin, cos, 0],
                             [0, 0, 0, 1]])
    
    # rotationMat2 = np.array([[cos, -sin, 0, 0],
    #                          [sin, cos, 0, 0],
    #                          [0, 0, 1, 0],
    #                          [0, 0, 0, 1]])
    
    translationMat = np.array([[1, 0, 0, 0],
                               [0, 1, 0, 0],
                               [0, 0, 1, (l2_l3 + l10)],
                               [0, 0, 0, 1]])
    
    step1 = np.matmul(rotationMat1, coordsFromCamera)
    print('step1', step1)
    #step2 = np.matmul(rotationMat2, step1)
    #print('step2', step2)
    coordsFromBase = np.matmul(translationMat, step1) 
    
    return coordsFromBase[:-1]


##############################################################

def detectionLoop(color):
    
    inVideo = cv2.VideoCapture(0,cv2.CAP_V4L2)
    inVideo.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y', '1', '6', ' '))
    inVideo.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    inVideo.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    
    
    if inVideo.read()[0]:
        print('Camera index correct')
    
    #inVideo.set(cv2.CAP_PROP_FRAME_WIDTH,  1920)
    #inVideo.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    print(inVideo.get(cv2.CAP_PROP_FRAME_WIDTH),inVideo.get(cv2.CAP_PROP_FRAME_HEIGHT))

    xCoordList = []
    yCoordList = []
    
    start = time.time()
    #print('start',start)
    
    while (True):
        
        # numToColor = {
        #         1: "red",
        #         2: "green",
        #         3: "blue"
        #     }
        
        #color = numToColor[colorNumber]
        
        _, img =  inVideo.read()
        hsvImg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        mask = createMask(color, hsvImg)
        
        kernel = np.ones((3,3), np.uint8)
        
        andMask = cv2.bitwise_and(img, img, mask = mask)
        
        contours = contourDefinition(andMask, kernel)
        
        xWorld, yWorld = identifying(contours, color, img)
        print("Trying to identify")
        
        if type(xWorld) != str:
            
            xCoordList.append(xWorld)
            yCoordList.append(yWorld)
            #print(len(xCoordList))
            start = time.time()
            #print('start',start)
            
            if len(xCoordList) >= 25:
                confirmed = confirmDetection(xCoordList, yCoordList)
                
                if confirmed:
                    finalCoords = coordinateTransform(xWorld, yWorld)
                    
                    break
                
                else:
                    xCoordList = []
                    yCoordList = []
        #print(xWorld, yWorld)
                        
                        #cv2.drawContours(img,contoursBlue,-1,(255,255,255),3)                     
                        
        #cv2.imshow("Colors", img)
        #cv2.imshow("b",blueAnd)
        #cv2.imshow("b2",blueDilate)
        stop = time.time()
        #print(stop - start)
        
        if (stop - start > 3):
            xCoordList = []
            yCoordList = []
        
        if (stop - start > 10):
            finalCoords = []
            print("exit")
            break
        

    inVideo.release()
    cv2.destroyAllWindows()
    
    return finalCoords

#f = detectionLoop("green")
#print('final', f)
