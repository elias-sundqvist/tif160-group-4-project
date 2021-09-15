#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 16:20:15 2021

@author: angelobarona
"""

import numpy as np
import cv2

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
    
    kernel = np.ones((5,5), np.uint8)
    
    
    # redDilate = cv2.dilate(redMask, kernel, iterations=3)
    # redAnd = cv2.bitwise_and(img, img, mask = redDilate)
    
    # greenDilate = cv2.dilate(greenMask, kernel, iterations=3)
    # greenAnd = cv2.bitwise_and(img, img, mask = greenDilate)
    
    # blueDilate = cv2.dilate(blueMask, kernel, iterations=3)
    # blueAnd = cv2.bitwise_and(img, img, mask = blueDilate)
    
    colors = [redMask, greenMask, blueMask]
    colorContours = []
    
    for color in colors:
        dilation = cv2.dilate(color,kernel,iterations=3)
        erosion = cv2.erode(dilation,kernel,iterations=3)
        smooth = cv2.GaussianBlur(erosion,(5,5),0)
        canny = cv2.Canny(smooth,100,200)
        contours,_ = cv2.findContours(np.array(canny),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        colorContours.append(contours)
        
    contoursRed, contoursGreen, contoursBlue = colorContours
    
    
    # contoursRed, hierarchyRed = cv2.findContours(redDilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # contoursGreen, hierarchyGreen = cv2.findContours(greenDilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # contoursBlue, hierarchyBlue = cv2.findContours(blueDilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    
    for i, contour in enumerate(contoursRed):
        perimeter = 0.1 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, perimeter, True)
                
        if len(approx) == 4:
            
            area = cv2.contourArea(contour)
            
            if(area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                ratio = w / float(h)
                
                if (0.95 <= ratio <= 1.05):
                    img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                  
                cv2.putText(img, "Red Color", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255))
    
    
    for i, contour in enumerate(contoursGreen):
        perimeter = 0.1 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, perimeter, True)
                
        if len(approx) == 4:
            
            area = cv2.contourArea(contour)
            
            if(area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                ratio = w / float(h)
                
                if (0.95 <= ratio <= 1.05):
                    img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                cv2.putText(img, "Green Color", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0))
            
    
    for i, contour in enumerate(contoursBlue):
        perimeter = 0.1 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, perimeter, True)
                
        if len(approx) == 4:
            
            area = cv2.contourArea(contour)
            
            if(area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                ratio = w / float(h)
                
                if (0.95 <= ratio <= 1.05):
                    img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                  
                cv2.putText(img, "Blue Color", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0))
    
    cv2.imshow("Colors", img)
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        
        break
    
inVideo.release()
cv2.destroyAllWindows()