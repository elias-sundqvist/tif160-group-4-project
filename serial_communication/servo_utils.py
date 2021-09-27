from math import pi
from serial_communication.servo_ids import *

# Min/Max servo values (got from Arduino code)
MIN_MAX_VALUES = {BODY:[560, 2330],
                  NECK_PAN:[750, 2200],
                  NECK_TILT:[550, 2400],
                  SHOULDER:[550, 2150],
                  ELBOW:[550, 2340],
                  GRIP:[950, 2400]}

# SERVO_FOR_MIN_RAD, SERVO_FOR_MAX_RAD, MIN_RAD, MAX_RAD
MIN_MAX_SERVO_RAD = {
    BODY: [950,1900,-pi/4,pi/4],
    SHOULDER: [2180, 1280, 0, pi/2],
    ELBOW: [1400, 2400, 0, pi/2],
    NECK_PAN: [550, 2300, -pi/2, pi/2],
    NECK_TILT: [2350, 1000, -pi/4, pi/2]
}

GRIPPER_VALUES = {'red':1160,
                  'blue':1250}

def servo_to_rad(servo, servo_value):
    min_serv, max_serv, min_rad, max_rad = MIN_MAX_SERVO_RAD[servo]
    a = (servo_value - max_serv)/(min_serv - max_serv)
    return a * (min_rad - max_rad) + max_rad

def rad_to_servo(servo, radians):
    min_serv, max_serv, min_rad, max_rad = MIN_MAX_SERVO_RAD[servo]
    a = (radians - max_rad)/(min_rad - max_rad)
    return int(a * (min_serv - max_serv) + max_serv)

def body_to_deg(body_servo):
    m = 9970/7
    k = 72/7
    return (body_servo-m)/k

def pan_to_deg(pan_servo):
    m = 1425
    k = 175/18
    return (pan_servo-m)/k

def tilt_to_deg(tilt_servo):
    m = 1870
    k = -29/3
    return (tilt_servo-m)/k

def shoulder_to_deg(shoulder_servo):
    m = 2180
    k = -10
    return (shoulder_servo-m)/k

def elbow_to_deg(elbow_servo):
    m = 1400
    k = 100/9
    return (elbow_servo-m)/k


