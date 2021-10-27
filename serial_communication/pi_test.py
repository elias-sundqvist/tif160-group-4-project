# Serial communication code for Raspberry pi
# Intened use is between a Pi <-> Arduino via USB serial
# Created by Martin Asplund - 10/09/21
import serial
import time
from threading import Thread, Event
from serial_communication.servo_ids import *

hubert_dict = {BODY: 560,
              NECK_PAN: 1425,
              NECK_TILT: 1870,
              SHOULDER: 2180,
              ELBOW: 1400,
              GRIP: 1700,
              READY: False}

diff_dict = {LEFT_WHEEL: 0,
             RIGHT_WHEEL: 0,
             SPEED_DUR: 0,
             READY_diff: False}


class TimerThreadWrite(Thread):
    def __init__(self, event, bus_hubert, bus_diff, agent, interval=1.2):
        Thread.__init__(self)
        self.stopped = event
        self.interval = interval
        self.bus_hubert = bus_hubert
        self.bus_diff = bus_diff
        self.agent = agent
    
    def run(self):
        # Thread to send messages over UART
        while not self.stopped.wait(self.interval):
            try:
                global hubert_dict
                global diff_dict
                if(hubert_dict[READY] and diff_dict[READY_diff]): # This condition could still work for both Arduino's, so we are not moving forward/bakwards when hubert is moving his arm
                    # print("Sending new pos!")
                    temp_dict = {**hubert_dict, **diff_dict}
                    #print("Calling agent for next task?")
                    new_positions = self.agent.run(temp_dict)
                    #print(f"new_positions: {new_positions}")
                    res = ''
                    for i, item in enumerate(new_positions):
                        res += str(item) + ':' + str(new_positions[item]) + ('' if i == len(new_positions)-1 else '&') # This will add a '&' to the last servo also, might remove it
                    #print(f"Sending new pos: {res}")
                    self.bus_hubert.write(res.encode('utf-8'))
                    self.bus_diff.write(res.encode('utf-8'))

            except (serial.SerialException or TypeError) as e: # Not sure this is allowed (BUG)
                #There is no new data from serial port
                print("Write serial error got ",e)
                #self.bus.flush()
                #continue
                self.bus_hubert.close()
                self.bus_diff.close()
                self.stopped.set() # This will close the thread

class TimerThreadRead(Thread):
    def __init__(self, event, bus_diff, bus_hubert, interval=0.1): # Might change the interval to be the same as Arduino write
        Thread.__init__(self)
        self.stopped = event
        self.interval = interval
        self.bus_diff = bus_diff
        self.bus_hubert = bus_hubert
    
    def run(self):
        # Thread to read messages over UART-usb
        while not self.stopped.wait(self.interval):
            try:
                line_1 = self.bus_hubert.readline().decode('utf-8').rstrip() # Read for 'timeout' time [sec] or until all the data is recived
                line_2 = self.bus_diff.readline().decode('utf-8').rstrip()
                                                                    
                commands_1 = line_1.split('&') # Split at '&' so we will have 'servo1:data&servo2:data&etc..'
                commands_2 = line_2.split('&')

                global hubert_dict
                global diff_dict

                for command in commands_1:
                    try:
                        temp = command.split(':')
                        servo = temp[0]
                        value = temp[1]
                        if servo in hubert_dict:
                            hubert_dict[servo] = (int(value) if servo != 6 else bool(value)) #We could store them as strings and deal with int convertion later in agent?
                    except:
                        continue # This is only for the first time reading the Arduino might give strange things
                
                for command in commands_2:
                    try:
                        temp = command.split(':')
                        servo = temp[0]
                        value = temp[1]
                        if servo in diff_dict:
                            diff_dict[servo] = int(value)
                    except:
                        continue # This is only for the first time reading the Arduino might give strange things
                #print(hubert_dict)
                #print(diff_dict)

            except (serial.SerialException or TypeError) as e: # Not sure this is allowed (BUG)
                #There is no new data from serial port
                print("Read serial error got ",e)
                self.bus_hubert.close()
                self.bus_diff.close()
                self.stopped.set() # This will close the thread
                #self.bus = serial.Serial('/dev/ttyACM0', 57600, timeout=0) # If the name is not the arduino test '/dev/ttyUSB0' [This is for USB communication! if I2C is used name need to be changed]
                #self.bus.flush()


class SerialCommunicator:
    def __init__(self, agent):
        # If the name is not the arduino test '/dev/ttyUSB0' [This is for USB communication! if I2C is used name need to be changed]
        # These adresses might change, it depends on which Arduino we connect first
        # This is for the diff. Arduino
        self.bus_diff = serial.Serial('/dev/ttyACM0', 57600, timeout=0) 
        # This is for the Hubert Arduino
        self.bus_hubert = serial.Serial('/dev/ttyACM1', 57600, timeout=0)
    
        # Flush both of the buses
        self.bus_diff.flush()
        self.bus_hubert.flush()

        # Start the read thread
        thread_stopped_read = Event()
        self.thread_read = TimerThreadRead(thread_stopped_read, self.bus_diff, self.bus_hubert)
        self.thread_read.name = 'Read thread'
        self.thread_read.start()

        time.sleep(1) # Sleep for some time to fill the dict with data (Kinda dependent if the Arduino has started or not)

        # Start UART-write thread
        thread_stopped_write = Event()
        self.thread_write = TimerThreadWrite(thread_stopped_write, self.bus_hubert, self.bus_diff, agent)
        self.thread_write.name = 'Write thread'
        self.thread_write.start()

        # thread_write.join() # Join the write thread to main so that main thread will stay active until write thread ends
        # self.bus.close()
        # print("Terminating...")
        # time.sleep(1)
