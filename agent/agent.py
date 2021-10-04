from serial_communication.servo_utils import MIN_MAX_VALUES
import kinematics.kinematics as k
from serial_communication.servo_ids import *
from serial_communication.servo_utils import servo_to_rad, rad_to_servo
from math import pi

THRESHOLD=20

poses = [
    {
        BODY: 0,
        SHOULDER: 0,
        ELBOW: 0,
        GRIP: 1700
    },
    {
        BODY: 0.8*pi / 2,
        SHOULDER: pi / 8,
        ELBOW: pi / 8,
        GRIP: 700
    },
    
    {
        BODY: 0.8*pi / 2,
        SHOULDER: pi / 8,
        ELBOW: pi / 8,
        GRIP: 1200
    },

    {
        BODY: 0.8*pi / 2,
        SHOULDER: pi / 8,
        ELBOW: pi /2,
        GRIP: 1200
    }
]



class Agent():
    def __init__(self):
        self.placeholder = -1
        self.state = 0

    def run(self, dict, target):
        new_dict = {}
        # target_pose = poses[self.state]
        # done = True
        # for k in target_pose.keys():
        #     target_servo_val = rad_to_servo(k, target_pose[k]) if k != GRIP else target_pose[k]
        #     #print(dict[k], target_servo_val, k)

        #     if(abs(dict[k]-target_servo_val)>THRESHOLD):
        #         done=False

        #     new_dict[k] = target_servo_val

        
        # if done:
        #     self.state+=1
        # #print(self.state)

        body_rad, shoulder_rad, elbow_rad = k.step_towards_target([
                servo_to_rad(BODY,dict[BODY]),
                servo_to_rad(SHOULDER,dict[SHOULDER]),
                servo_to_rad(ELBOW,dict[ELBOW])
        ], target, 50, 0.9)
        print(f"Body: {body_rad} Shoulder {shoulder_rad} Elbow {elbow_rad}")
        # if(abs(dict[BODY] - rad_to_servo(BODY, body_rad))<THRESHOLD):
        #     if(abs(dict[SHOULDER] - rad_to_servo(SHOULDER, shoulder_rad))<THRESHOLD):
        #         new_dict[ELBOW] = rad_to_servo(ELBOW, elbow_rad)
        #     new_dict[SHOULDER] = rad_to_servo(SHOULDER, shoulder_rad)
        # new_dict[BODY] = rad_to_servo(BODY, body_rad)
        new_dict[BODY] = rad_to_servo(BODY, body_rad)
        new_dict[SHOULDER] = rad_to_servo(SHOULDER, shoulder_rad)
        new_dict[ELBOW]  = rad_to_servo(ELBOW, elbow_rad)

        # for item in dict:
        #     if dict[item] < MIN_MAX_VALUES[item][0]:
        #         dict[item] = MIN_MAX_VALUES[item][0]
        #     elif dict[item] > MIN_MAX_VALUES[item][1]:
        #         dict[item] = MIN_MAX_VALUES[item][1]

        return new_dict

    def fetch(self, color):
        print(f"Fetching {color}")
