from serial_communication.servo_utils import MIN_MAX_VALUES
from serial_communication.servo_ids import *
from agent import tasks
from color_detection.objectDetection import detectionLoop
from buzzer import buzzer 
from cascade_classifier.HandDetection import handDetection

import numpy as np

class Agent:
    def __init__(self):
        self.taskList = [tasks.MoveHandToPosition([0.103,0.26625,0.51925])]
        self.task = tasks.WaitForInstructions()

    def run(self, dict):
        self.task.run(self, dict)
        if self.task.is_done(dict):
            if len(self.taskList) > 0:
                self.task = self.taskList.pop(0)
            else:
                self.task = tasks.WaitForInstructions()

    def close_gripper(self, dict):
        return {**dict, GRIP: 950}

    def is_in_pose(self, current_pose, target, threshold=20):
        result = True
        for servo in target.keys():
            if abs(target[servo] - current_pose[servo]) > threshold:
                result = False
        return result

    def handle_speech(self, msg):
        msg = msg.lower()
        if 'cancel' in msg:
            self.taskList = []
            self.task = tasks.WaitForInstructions()

        if 'red' in msg:
            self.fetch('red')

        if 'green' in msg:
            self.fetch('green')

        if 'blue' in msg:
            self.fetch('blue')

    def fetch(self, color):
        print(f"Looking for {color}")
        cube_position = detectionLoop(color)
        buzzer.thinking_noise()
        if len(cube_position) == 3:
            self.taskList.append(tasks.OpenGrip())
            self.taskList.append(tasks.MoveHandToPosition(np.add(cube_position,[0,0,0.04])))
            self.taskList.append(tasks.MoveHandToPosition(cube_position))
            self.taskList.append(tasks.CloseGrip())                  
            self.taskList.append(tasks.MoveHandToPosition(np.add(cube_position,[0,0,0.04])))                     
            print(f"Coordinates: {cube_position}")
            print(f"Fetching {color}")
            buzzer.happy_noise()
        else:
            buzzer.sad_noise()

    def dropOffCube(self):
        print(f"Looking for Hand")

        #Modify theese:
        #-----------------------------------------------------------------------------------------
        steerCorrFactor = 1
        tiltCorrFactor = 1
        speedCorrFactor = 1

        steeringCorrMin = 0
        tiltCorrMin = 0
        speedCorrMin = 0

        steerCorrMax = 10
        tiltCorrMax = 10
        speedCorrMax = 10

        handWidthRatio = 0.3    #The ratio handWidth/frameWidth when the hand is close enough to drop the cube
        #-----------------------------------------------------------------------------------------

        steerCorr, tiltCorr, speedCorr, xHand, yHand = handDetection(handWidthRatio)

        #Multiplies the correction by a facor
        steerCorr = steerCorr * steerCorrFactor   #positive to the right
        tiltCorr  = tiltCorr * tiltCorrFactor     #I think this is positive downwards if (0,0) is in the top left corner
        speedCorr = speedCorr * speedCorrFactor

        #Sets Corr to 0 or CorrMax if the value is outside of [CorrMin-CorrMax]
        steerCorr = (steerCorrMin < abs(steerCorr) and abs(steerCorr) < steerCorrMax) * steerCorr  +  (abs(steerCorr) > steerCorrMax) * steerCorrMax
        tiltCorr  = ( tiltCorrMin < abs( tiltCorr) and abs( tiltCorr) <  tiltCorrMax) * tiltCorr   +  (abs( tiltCorr) >  tiltCorrMax) *  tiltCorrMax
        speedCorr = (speedCorrMin < abs(speedCorr) and abs(speedCorr) < speedCorrMax) * speedCorr  +  (abs(speedCorr) > speedCorrMax) * speedCorrMax


        if (steerCorrection==0 and tiltCorrection==0 and speedCorrection==0):
            hand_position = [xHand,yHand]
            #Dont know how to get z-coordinate, but needs to be done here
            if len(cube_position) == 3:
                self.taskList.append(tasks.MoveHandToPosition(hand_position))
                self.taskList.append(tasks.OpenGrip())               
                self.taskList.append(tasks.MoveHandToPosition(np.add(hand_position,[0,0,0.04])))    
                self.taskList.append(tasks.CloseGrip()) 
                print(f"Coordinates: {hand_position}")
                print(f"Dropped Cube at location")
                buzzer.happy_noise()
            else:
                buzzer.sad_noise()
        
        else:
            #Set speed based on SetWheelSpeeds()  (dont know how you have changed this)
            self.taskList.append(task.SetWheelSpeeds())
            