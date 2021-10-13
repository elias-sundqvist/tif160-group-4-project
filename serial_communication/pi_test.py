# Serial communication code for Raspberry pi
# Intened use is between a Pi <-> Arduino via USB serial
# Created by Martin Asplund - 10/09/21

import serial
import time
from threading import Thread, Event
from serial_communication.servo_ids import *

local_dict = {BODY: 560,
              NECK_PAN: 1425,
              NECK_TILT: 1870,
              SHOULDER: 2180,
              ELBOW: 1400,
              GRIP: 1700,
              READY: False}

class TimerThreadWrite(Thread):
    def __init__(self, event, bus, agent, interval=2):
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
                if(local_dict[READY]):
                    # print("Sending new pos!")
                    new_positions = self.agent.run(local_dict)
                    res = ''
                    for i, item in enumerate(new_positions):
                        res += str(item) + ':' + str(new_positions[item]) + ('' if i == len(new_positions)-1 else '&') # This will add a '&' to the last servo also, might remove it
                    print(f"Sending new pos: {res}")
                    self.bus.write(res.encode('utf-8'))

            except (serial.SerialException or TypeError) as e: # Not sure this is allowed (BUG)
                #There is no new data from serial port
                print("Write serial error got ",e)
                self.bus.close()
                self.stopped.set() # This will close the thread

class TimerThreadRead(Thread):
    def __init__(self, event, bus, interval=0.4): # Might change the interval to be the same as Arduino write
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
                    try:
                        temp = command.split(':')
                        servo = temp[0]
                        value = temp[1]
                        if servo in local_dict:
                            local_dict[servo] = (int(value) if servo != 6 else bool(value)) #We could store them as strings and deal with int convertion later in agent?
                    except:
                        continue # This is only for the first time reading the Arduino might give strange things
                #print(local_dict)

            except (serial.SerialException or TypeError) as e: # Not sure this is allowed (BUG)
                #There is no new data from serial port
                print("Read serial error got: ",e)
                self.bus.close()
                self.bus = serial.Serial('/dev/ttyACM0', 57600, timeout=0) # If the name is not the arduino test '/dev/ttyUSB0' [This is for USB communication! if I2C is used name need to be changed]
                self.bus.flush()
                #self.stopped.set() # This will close the thread


class SerialCommunicator:
    def __init__(self, agent):
        self.bus = serial.Serial('/dev/ttyACM0', 57600, timeout=0) # If the name is not the arduino test '/dev/ttyUSB0' [This is for USB communication! if I2C is used name need to be changed]
        self.bus.flush()

        # Start the read thread
        thread_stopped_read = Event()
        self.thread_read = TimerThreadRead(thread_stopped_read, self.bus)
        self.thread_read.name = 'Read thread'
        self.thread_read.start()

        time.sleep(1) # Sleep for some time to fill the dict with data (Kinda dependent if the Arduino has started or not)

        # Start UART-write thread
        thread_stopped_write = Event()
        self.thread_write = TimerThreadWrite(thread_stopped_write, self.bus, agent)
        self.thread_write.name = 'Write thread'
        self.thread_write.start()

        # thread_write.join() # Join the write thread to main so that main thread will stay active until write thread ends
        # self.bus.close()
        # print("Terminating...")
        # time.sleep(1)
