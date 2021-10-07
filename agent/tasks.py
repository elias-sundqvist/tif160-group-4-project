import torch

from agent.agent import Agent
from serial_communication.servo_utils import servo_to_rad, rad_to_servo
from serial_communication.servo_ids import *
import kinematics.kinematics as k
from math import pi

class Task:
    def run(self, agent: Agent, current_pose: dict):
        pass

    def is_done(self, agent: Agent, current_pose: dict):
        return True

class WaitForInstructions(Task):
    def run(self, agent: Agent, current_pose: dict):
        pass

    def is_done(self, agent: Agent, current_pose: dict):
        return True

class MoveHandToPosition(Task):
    def __init__(self, target):
        self.target = target

    def get_joint_angles(self, current_pose: dict):
        return [
            servo_to_rad(BODY, current_pose[BODY]),
            servo_to_rad(SHOULDER, current_pose[SHOULDER]),
            servo_to_rad(ELBOW, current_pose[ELBOW])
        ]

    def run(self, agent: Agent, current_pose: dict):
        new_dict = {}

        body_rad, shoulder_rad, elbow_rad = k.step_towards_target(self.get_joint_angles(current_pose), self.target, 50, 0.9)
        new_dict[BODY] = rad_to_servo(BODY, body_rad)
        new_dict[SHOULDER] = rad_to_servo(SHOULDER, shoulder_rad)
        new_dict[ELBOW] = rad_to_servo(ELBOW, elbow_rad)

        return new_dict

    def is_done(self, agent: Agent, current_pose: dict):
        with torch.no_grad:
            pos = k.forward(self.get_joint_angles(current_pose))
            distance = torch.mean(torch.square(torch.sub(pos, self.target)))
            return distance < 0.005