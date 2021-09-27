from serial_communication.servo_utils import MIN_MAX_VALUES
import kinematics.kinematics as k
from serial_communication.servo_ids import *
from serial_communication.servo_utils import servo_to_rad, rad_to_servo

class Agent():
    def __init__(self):
        self.placeholder = -1


    def run(self, dict, target):
        if target is not None:
            dict[BODY], dict[SHOULDER], dict[ELBOW] = map(rad_to_servo, k.step_towards_target([
                 servo_to_rad(dict[BODY]),
                 servo_to_rad(dict[SHOULDER]),
                 servo_to_rad(dict[ELBOW])
            ], target, 100))

        for item in dict:
            if dict[item] < MIN_MAX_VALUES[item][0]:
                dict[item] = MIN_MAX_VALUES[item][0]
            elif dict[item] > MIN_MAX_VALUES[item][1]:
                dict[item] = MIN_MAX_VALUES[item][1]

        return dict

    def fetch(self, color):
        print(f"Fetching {color}")