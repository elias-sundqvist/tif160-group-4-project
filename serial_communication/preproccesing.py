# Servo ID's
BODY      = '0'
NECK_PAN  = '1'
NECK_TILT = '2'
SHOULDER  = '3'
ELBOW     = '4'
GRIP      = '5'

# Min/Max servo values (got from Arduino code)
MIN_MAX_VALUES = {BODY:[560, 2330],
                  NECK_PAN:[750, 2200],
                  NECK_TILT:[550, 2400],
                  SHOULDER:[550, 2150],
                  ELBOW:[550, 2340],
                  GRIP:[950, 2400]}

GRIPPER_VALUES = {'red':1160,
                  'blue':1250}

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


class Agent():
    def __init__(self):
        self.placeholder = -1
        

    def run(self, dict):
        for item in dict:
            if( dict[item] < MIN_MAX_VALUES[item][1] ):
                dict[item] = MIN_MAX_VALUES[item][1]
            else:
                dict[item] = MIN_MAX_VALUES[item][0]
            
        return dict
