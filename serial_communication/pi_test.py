# Serial communication code for Raspberry pi
# Intened use is between a Pi <-> Arduino via USB serial
# Created by Martin Asplund - 10/09/21

import serial
import time
import preproccesing
from datetime import datetime
from threading import Thread, Event

# Servo ID's
BODY = 0
NECK_PAN = 1
NECK_TILT = 2
SHOULDER = 3
ELBOW = 4
GRIP = 5

local_dict = {BODY: 0.0,
              NECK_PAN: 0.0,
              NECK_TILT: 0.0,
              SHOULDER: 0.0,
              ELBOW: 0.0,
              GRIP: 0.0}

class TimerThreadWrite(Thread):
    def __init__(self, event, bus, agent, interval=0.05):
        Thread.__init__(self)
        self.stopped = event
        self.interval = interval
        self.bus = bus
        self.agent = agent
    
    def run(self):
        # Thread to send messages over UART
        while not self.stopped.wait(self.interval):
            try:
                global local_dict
                new_positions = self.agent.run(local_dict)
                res = ''
                for item in new_positions:
                    res += str(item) + ':' + str(new_positions[item]) + '&' # This will add a '&' to the last servo also, might remove it
                bus.write(res.encode('utf-8'))

            except serial.SerialException or TypeError as e: # Not sure this is allowed
                #There is no new data from serial port
                print("Serial error got ",e)
                self.bus.close()
                self.stopped.set() # This will close the thread

class TimerThreadRead(Thread):
    def __init__(self, event, bus, interval=0): # Might change the interval to be the same as Arduino write
        Thread.__init__(self)
        self.stopped = event
        self.interval = interval
        self.bus = bus
    
    def run(self):
        # Thread to read messages over UART-usb
        while not self.stopped.wait(self.interval):
            try:
                line = self.bus.readline().decode('utf-8').rstrip() # Read for 'timeout' time [sec] or until all the data is recived
                                                                    # Should add that the thread terminates if the it cant write/read
                commands = line.split('&') # Split at '&' so we will have 'servo1:data&servo2:data&etc..'
                global local_dict
                for command in commands:
                    temp = command.split(':')
                    sensor = temp[0]
                    value = temp[1]
                    local_dict[sensor] = value

            except (serial.SerialException or TypeError) as e: # Not sure this is allowed
                #There is no new data from serial port
                print("Serial error got: ",e)
                self.bus.close()
                self.stopped.set() # This will close the thread


if __name__ == '__main__':
    bus = serial.Serial('/dev/ttyACM0', 57600, timeout=1) # If the name is not the arduino test '/dev/ttyUSB0' [This is for USB communication! if I2C is used name need to be changed]
    bus.flush()
    agent = preproccesing.Agent() # This will be the preproccesing agent that will take all the inputs and process the new output
                                  # This is so if we need specific parameters for the agent and also if we want to create different agents for Hubert to try out different motions

    # Start the read thread
    thread_stopped_read = Event()
    thread_read = TimerThreadWrite(thread_stopped_read,bus)
    thread_read.name = 'Read thread'
    thread_read.start()

    time.sleep(1) # Sleep for some time to fill the dict with data (Kinda dependent if the Arduino has started or not)
    
    # Start UART-write thread
    thread_stopped_write = Event()
    thread_write = TimerThreadWrite(thread_stopped_write,bus,agent)
    thread_write.name = 'Write thread'
    thread_write.start()

    thread_write.join() # Join the write thread to main so that main thread will stay active until write thread ends
    bus.close()
    print("Terminating...")
    time.sleep(1)