#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 19:16:47 2021

@author: angelobarona
"""

from objectDetection import detectionLoop

#if speechOutput in [1,2,3]:
x,y = detectionLoop(3)
print(x,y)