from serial_communication.servo_utils import MIN_MAX_VALUES
from serial_communication.servo_ids import *
from agent.tasks import *
from color_detection.objectDetection import detectionLoop
from color_detection.objectDetection import coordinateTransform
from buzzer import buzzer 
from cascade_classifier.Hand_Detection import handDetection

import numpy as np

class Agent:
    def __init__(self):
        self.taskList = [MoveHandToPosition([0.103,0.26625,0.51925])]
        self.task = WaitForInstructions()

    def run(self, dict):
        self.task.run(self, dict)
        if self.task.is_done(dict):
            if len(self.taskList) > 0:
                self.task = self.taskList.pop(0)
            else:
                self.task = WaitForInstructions()

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
            self.task = WaitForInstructions()

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
            self.taskList.append(OpenGrip())
            self.taskList.append(MoveHandToPosition(np.add(cube_position,[0,0,0.04])))
            self.taskList.append(MoveHandToPosition(cube_position))
            self.taskList.append(CloseGrip())                  
            self.taskList.append(MoveHandToPosition(np.add(cube_position,[0,0,0.04])))                     
            print(f"Coordinates: {cube_position}")
            print(f"Fetching {color}")
            buzzer.happy_noise()
        else:
            buzzer.sad_noise()

    def dropOffCube(self):
        print(f"Looking for Hand")

        # OBS!!: Modify theese:
        #-----------------------------------------------------------------------------------------
        steerCorrFactor = 1     #How much it turns for each pixel it's off to the side
        tiltCorrFactor = 1      #How much it tilts -||-
        speedCorrFactor = 200   #How much the speed changes based on handWidth/frameWidth

        steerMin = 10
        tiltMin = 10
        speedMin = 50

        steerMax = 40       #Max Steering   (ex: speedL=speedMax-steerMax, speedR=speedMax+steerMax)
        tiltMax = 400
        speedMax = 80

        handWidthRatio = 0.3    #The ratio handWidth/frameWidth when the hand is close enough to drop the cube
        #-----------------------------------------------------------------------------------------

        steerCorr, tiltCorr, speedCorr, xHand, yHand = handDetection(handWidthRatio)

        #Multiplies the correction by a facor
        steer = steerCorr * steerCorrFactor         #positive to the right
        tilt  = tiltCorr * tiltCorrFactor           #I think this is positive downwards if (0,0) is in the top left corner
        speed = round(speedCorr * speedCorrFactor)  

        #Sets Corr to 0 or +-Max if the value is outside of [CorrMin-CorrMax]
        if (steer > steerMax):
            steer = steerMax
        elif (steer < -steerMax):
            steer = -steerMax
        elif (abs(steer) < steerMin):
            steer = 0

        if (tilt > tiltMax):
            tilt = tiltMax
        elif (tilt < -tiltMax):
            tilt = -tiltMax
        elif (abs(tilt) < tiltMin):
            tilt = 0

        if (speed > speedMax):
            speed = speedMax
        elif (speed < -speedMax):
            speed = -speedMax
        elif (abs(speed) < speedMin):
            speed = 0


        if (steerCorrection==0 and tiltCorrection==0 and speedCorrection==0):
            hand_position = coordinateTransform(xHand,yHand)

            if len(hand_position) == 3:
                self.taskList.append(MoveHandToPosition(hand_position))
                self.taskList.append(OpenGrip())               
                self.taskList.append(MoveHandToPosition(np.add(hand_position,[0,0,0.04])))    
                self.taskList.append(CloseGrip()) 
                print(f"Coordinates: {hand_position}")
                print(f"Dropped Cube at location")
                buzzer.happy_noise()
            else:
                buzzer.sad_noise()
        
        else:
            #Set speed based on SetWheelSpeeds()  (dont know how you have changed this)
            self.taskList.append(task.SetWheelSpeeds(speed+steer,speed-steer,4))    #Guessing 4 is good, you can change it
            
            #Tilt camera based on tiltCorr here:
            