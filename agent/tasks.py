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
        print(f"Requested: {new_dict}")
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

class SetAngle(Task):
    def __init__(self, servos, angles):
        self.servo = servos
        self.target_servo_value = [rad_to_servo(servo, angle) for (servo, angle) in zip(servos, angles)]
        self.new_dict = {}

    def run(self, agent, current_pose: dict):

        for (servo, value) in zip(self.servo, self.target_servo_value):
            self.new_dict[servo] = value
        return self.new_dict
    
    def is_done(self, agent, current_pose):
        return agent.is_in_pose(current_pose, self.new_dict, threshold=20)


class ShakeTorso(Task):
    def __init__(self, iters, amount):
        self.start_angle = None
        self.iters = iters
        self.amount = amount
        self.sign = 1

    def run(self, agent, current_pose: dict):
        self.new_dict = {}

        if self.start_angle is None:
            self.start_angle = current_pose[BODY]

        if self.iters > 0:
            self.iters = self.iters - 1
            self.new_dict[BODY] = self.start_angle + self.sign * self.amount
            self.sign = self.sign * -1
        else:
            self.new_dict[BODY] = self.start_angle

        return self.new_dict
    
    def is_done(self, agent, current_pose):
        return self.iters <= 0 and agent.is_in_pose(current_pose, self.new_dict, threshold=20)


class OpenHand(Task):
    def run(self, agent, current_pose):
        print("Opening Gripper")
        return {**current_pose, GRIP: 650}

    def is_done(self, agent, current_pose):
        return agent.is_in_pose(current_pose, {GRIP: 650}, threshold=50)

class CloseHand(Task):
    def run(self, agent, current_pose):
        print("Closing Gripper")
        return {**current_pose, GRIP: 1150}

    def is_done(self, agent, current_pose):
        return agent.is_in_pose(current_pose, {GRIP: 1150}, threshold=50)

class SetWheelSpeeds(Task):
    def __init__(self, leftSpeed, rightSpeed, duration):
        self.targetSpeed = [leftSpeed, rightSpeed, duration]
        self.did_reach_target=False
        

    def run(self, agent, current_speeds: dict):
        new_dict = {}

        new_dict[LEFT_WHEEL] = self.targetSpeed[0]
        new_dict[RIGHT_WHEEL] = self.targetSpeed[1]
        new_dict[SPEED_DUR] = self.targetSpeed[2]

        return new_dict
    
    def is_done(self, agent, current_pose):
        return current_pose[LEFT_WHEEL]==0 and current_pose[RIGHT_WHEEL]==0
            
        
class CallFunction(Task):
    def __init__(self, func):
        self.func = func
        self.is_done_val = False
    
    def run(self, agent, current_speeds: dict):
        self.is_done_val = self.func()
        return {}
    
    def is_done(self, agent, current_pose):
        return self.is_done_val