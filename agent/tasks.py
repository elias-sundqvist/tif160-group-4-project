import torch

from serial_communication.servo_utils import servo_to_rad, rad_to_servo
from serial_communication.servo_ids import *
import kinematics.kinematics as k
from math import pi

class Task:
    def run(self, agent, current_pose: dict):
        pass

    def is_done(self, agent, current_pose: dict):
        return True

class WaitForInstructions(Task):
    def run(self, agent, current_pose: dict):
        return {}

    def is_done(self, agent, current_pose: dict):
        return True

class MoveHandToPosition(Task):
    def __init__(self, target):
        self.target = target
        self.last_new_dict = None

    def get_joint_angles(self, current_pose: dict):
        return [
            servo_to_rad(BODY, current_pose[BODY]),
            servo_to_rad(SHOULDER, current_pose[SHOULDER]),
            servo_to_rad(ELBOW, current_pose[ELBOW])
        ]

    def run(self, agent, current_pose: dict):
        new_dict = {}

        body_rad, shoulder_rad, elbow_rad = k.step_towards_target(self.get_joint_angles(current_pose), self.target, 50, 0.9)
        new_dict[BODY] = rad_to_servo(BODY, body_rad)
        new_dict[SHOULDER] = rad_to_servo(SHOULDER, shoulder_rad)
        new_dict[ELBOW] = rad_to_servo(ELBOW, elbow_rad)
        self.last_new_dict = new_dict

        return new_dict

    def is_done(self, agent, current_pose: dict):
        
        θ = torch.tensor(self.get_joint_angles(current_pose), requires_grad=False)
        target_tensor = torch.tensor(self.target, requires_grad=False)
        pos = k.forward(θ)
        distance = torch.mean(torch.square(torch.sub(pos, target_tensor)))
        #print(f"distance: {distance}")
        is_done = distance < 0.005
        if is_done:
            print("movement done")
        #else:
        #    if  agent.is_in_pose(current_pose, self.last_new_dict):
       #         print("Target is out of reach... considering task done.")
       #         return True

        return is_done

class OpenHand(Task):
    def run(self, agent, current_pose):
        print("Opening Gripper")
        return {**current_pose, GRIP: 1000}

    def is_done(self, agent, current_pose):
        return agent.is_in_pose(current_pose, {GRIP: 1000})

class CloseHand(Task):
    def run(self, agent, current_pose):
        print("Closing Gripper")
        return {**current_pose, GRIP: 1500}

    def is_done(self, agent, current_pose):
        return agent.is_in_pose(current_pose, {GRIP: 1500})

