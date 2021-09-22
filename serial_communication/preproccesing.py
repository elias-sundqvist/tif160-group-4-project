# Servo ID's
BODY      = 0
NECK_PAN  = 1
NECK_TILT = 2
SHOULDER  = 3
ELBOW     = 4
GRIP      = 5

# Min/Max servo values (got from Arduino code)
MIN_MAX_VALUES = {
                  BODY:[560, 2330],
                  NECK_PAN:[750, 2200],
                  NECK_TILT:[550, 2400],
                  SHOULDER:[550, 2150],
                  ELBOW:[550, 2340],
                  GRIP:[950, 2400]
                 }

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