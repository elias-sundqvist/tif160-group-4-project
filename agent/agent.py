from serial_communication.servo_utils import MIN_MAX_VALUES
from serial_communication.servo_ids import *
from agent import tasks
from color_detection.objectDetection import detectionLoop
from buzzer import buzzer 
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
            self.taskList.append(tasks.OpenGripper())
            self.taskList.append(tasks.MoveHandToPosition(np.add(cube_position,[0,0,0.04)))
            self.taskList.append(tasks.MoveHandToPosition(cube_position))
            self.taskList.append(tasks.CloseGripper())                  
            self.taskList.append(tasks.MoveHandToPosition(np.add(cube_position,[0,0,0.04)))                     
            print(f"Coordinates: {cube_position}")
            print(f"Fetching {color}")
            buzzer.happy_noise()
        else:
            buzzer.sad_noise()
