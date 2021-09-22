#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 16:20:15 2021

@author: angelobarona
"""

import numpy as np
import cv2

def contourDefinition(andMask,kernel):
    dilation = cv2.dilate(andMask,kernel,iterations=3)
    #andMask = cv2.bitwise_and(hsvImg, hsvImg, mask = color)
    erosion = cv2.erode(dilation,kernel,iterations=3)
    smooth = cv2.GaussianBlur(erosion,(5,5),0)
    canny = cv2.Canny(smooth,100,200)
    contours,_ = cv2.findContours(np.array(canny),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    return contours


def giveMeColor(color):
    
    colorArray = {
            "red": (0, 0, 255),
            "green": (0, 255, 0),
            "blue": (255, 0, 0)
        }
    
    return colorArray[color]


def identifying(contours, color, image):
        
    colorA = giveMeColor(color)
    
    for i, contour in enumerate(contours):
        perimeter = 0.1 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, perimeter, True)
                
        if (len(approx) == 4 or len(approx) == 6):
            
            area = cv2.contourArea(contour)
            
            if(area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                ratio = w / float(h)
                                
                if ((0.95 <= ratio <= 1.05) or len(approx) == 6):
                    image = cv2.rectangle(image, (x, y), (x + w, y + h), colorA, 2)
                  
                    cv2.putText(image, color, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, colorA)
                    
                    moments = cv2.moments(contour)
                    
                    xCenter = int(moments['m10']/moments['m00'])
                    yCenter = int(moments['m01']/moments['m00'])
                    
                    cv2.drawMarker(image,(xCenter,yCenter), color=(255,255,255), markerType=cv2.MARKER_STAR)
    
    return True

##############################################################

inVideo = cv2.VideoCapture(0)

while (True):
    _, img =  inVideo.read()
    hsvImg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    redLowHsv = np.array([136, 87, 111], np.uint8)
    redHighHsv = np.array([180, 255, 255], np.uint8)
    redMask = cv2.inRange(hsvImg, redLowHsv, redHighHsv)
    
    greenLowHsv = np.array([25, 52, 72], np.uint8)
    greenHighHsv = np.array([102, 255, 255], np.uint8)
    greenMask = cv2.inRange(hsvImg, greenLowHsv, greenHighHsv)
    
    blueLowHsv = np.array([94, 80, 2], np.uint8)
    blueHighHsv = np.array([120, 255, 255], np.uint8)
    blueMask = cv2.inRange(hsvImg, blueLowHsv, blueHighHsv)
    
    kernel = np.ones((3,3), np.uint8)
    
    redAnd = cv2.bitwise_and(img, img, mask = redMask)
    #redDilate = cv2.dilate(redMask, kernel, iterations=3)
    
    greenAnd = cv2.bitwise_and(img, img, mask = greenMask)
    #greenDilate = cv2.dilate(greenMask, kernel, iterations=3)
    
    blueAnd = cv2.bitwise_and(img, img, mask = blueMask)
    #blueDilate = cv2.dilate(blueMask, kernel, iterations=3)
    
    contoursRed = contourDefinition(redAnd, kernel)
    contoursGreen = contourDefinition(greenAnd, kernel)
    contoursBlue = contourDefinition(blueAnd, kernel)
    
    identifying(contoursRed, "red", img)
    identifying(contoursGreen, "green", img)
    identifying(contoursBlue, "blue", img)
                    
                    #cv2.drawContours(img,contoursBlue,-1,(255,255,255),3)                     
                    
    cv2.imshow("Colors", img)
    #cv2.imshow("b",blueAnd)
    #cv2.imshow("b2",blueDilate)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        
        break
    
inVideo.release()
cv2.destroyAllWindows()