from serial_communication.servo_utils import MIN_MAX_VALUES, servo_to_rad
from serial_communication.servo_ids import *
from serial_communication.pi_test import hubert_dict
from agent import tasks
from color_detection.objectDetection import detectionLoop, find_index, coordinateTransform
from cascade_classifier.Hand_Detection import handDetection
from buzzer import buzzer
import numpy as np
import cv2
from math import pi

class Agent:
    def __init__(self):
        self.taskList = [tasks.MoveHandToPosition([0.103,0.049,0.068])]
        self.task = tasks.WaitForInstructions()
        self.camera = find_index()
        self.release = False

    def run(self, dict):
        #print(f"Calling run with dict {dict}")
        # if self.task.is_done(self, dict):
        #     print(f"task list len: {len(self.taskList)}")
        #     if len(self.taskList) > 0:
        #         self.task = self.taskList.pop(0)
        #     else:
        #         self.task = tasks.WaitForInstructions()
        
        res = self.task.run(self, dict)
        
        if self.task.is_done(self, dict):
            #print(f"task list len: {len(self.taskList)}")
            if len(self.taskList) > 0:
                self.task = self.taskList.pop(0)
                print(f"New Task: {type(self.task).__name__}")
            else:
                self.task = tasks.WaitForInstructions()
        return res

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
        def match(*words):
            for word in words:
                if word.lower() in msg:
                    return True
            return False

        if match('stop'):
            self.release = True

        if match('cancel','reset'):
            self.taskList = []
            self.task = tasks.MoveHandToPosition([0.103,0.049,0.068])
            self.taskList.append(tasks.SetAngle([NECK_TILT], [0]))
        
        if match('release','open'):
            self.taskList = []
            self.task = tasks.OpenHand()
     
        if match('grab','crab','close'):
            self.taskList = []
            self.task = tasks.CloseHand()

        if match('red', 'read', 'Brett', 'Rhett', 'rent','let', 'Bachelorette', 'pet', 'Shiba'):
            self.fetch('red')

        if match('green', 'Korean', 'screen', 'Kareem'):
            self.fetch('green')

        if match('blue'):
            self.fetch('blue')

        if match('right'):
            self.taskList = []
            self.task = tasks.SetWheelSpeeds(100,-100,1)
            buzzer.happy_noise()

        if match('left'):
            self.taskList = []
            self.task = tasks.SetWheelSpeeds(-100,100,1)
            buzzer.happy_noise()
        
        if match('forward', 'Fort Worth'):
            self.taskList = []
            self.task = tasks.SetWheelSpeeds(-100,-100,1)
            buzzer.happy_noise()

    def fetch(self, color):
        self.taskList.append(tasks.SetAngle([NECK_TILT], [pi/6]))
        print(f"Looking for {color}")
        buzzer.thinking_noise()
        cube_position = detectionLoop(self.camera, color, pi/6)
        print(f"cube position: {cube_position}")
        if len(cube_position) == 3:
            self.taskList.append(tasks.OpenHand())
            self.taskList.append(tasks.SetAngle([BODY, ELBOW, SHOULDER, NECK_TILT], [pi/4, pi/2, pi/2, 0]))
            #self.taskList.append(tasks.MoveHandToPosition(np.add(cube_position,[0,0,0.04])))
            self.taskList.append(tasks.MoveHandToPosition(np.add(cube_position,[0,0,0])))
            self.taskList.append(tasks.ShakeTorso(2,30))
            self.taskList.append(tasks.CloseHand())
            self.taskList.append(tasks.SetAngle([SHOULDER, ELBOW, BODY], [pi/2, pi/4, pi/4]))
            self.taskList.append(tasks.SetAngle([SHOULDER, ELBOW, BODY], [0, 0, pi/2]))
            self.taskList.append(tasks.SetWheelSpeeds(-100,100,15)) # Rotate 180 deg
            #self.taskList.append(tasks.SetWheelSpeeds(-100,-100,1)) # Drive forward
            #self.taskList.append(tasks.SetAngle([ELBOW], [pi/2]))
            self.taskList.append(tasks.CallFunction(lambda: self.dropOffCube()))
            #self.taskList.append(tasks.MoveHandToPosition(np.add(cube_position,[0,0,0.04]))) 
            print(f"Coordinates: {cube_position}")
            print(f"Fetching {color}")
            buzzer.happy_noise()
        else:
            buzzer.sad_noise()




 # David code
    def dropOffCube(self):
        print(f"Looking for Hand")

        # OBS!!: Modify theese:
        #-----------------------------------------------------------------------------------------
        steerCorrFactor = 0.02     #How much it turns for each pixel it's off to the side
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

        steerCorr, tiltCorr, speedCorr, xHand, yHand = handDetection(handWidthRatio,self.camera,self)

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

        # Need threshold here
        if (steer==0 and tilt==0 and speed==0):
           
            #self.taskList.append(tasks.MoveHandToPosition(hand_position))
            self.taskList.append(tasks.SetAngle([ELBOW], [pi/2]))
            self.taskList.append(tasks.OpenHand())               
            self.taskList.append(tasks.SetAngle([SHOULDER, ELBOW, BODY], [0, 0, pi/2]))  
            self.taskList.append(tasks.CloseHand()) 
            print(f"Dropped Cube at location")
            buzzer.happy_noise()
            return True
            
        else:
            #Set speed based on SetWheelSpeeds()  (dont know how you have changed this)
            print(f"LeftSpeed: {-speed-steer} RightSpeed: {-speed+steer}")
            self.taskList.append(tasks.SetWheelSpeeds(-speed+steer,-speed-steer,4))    #Guessing 4 is good, you can change it
            self.taskList.append(tasks.CallFunction(lambda: self.dropOffCube()))
            return True
            #Tilt camera based on tiltCorr here:
