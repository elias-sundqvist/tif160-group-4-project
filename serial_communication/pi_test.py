# Serial communication code for Raspberry pi
# Intened use is between a Pi <-> Arduino via USB serial
# Created by Martin Asplund - 10/09/21

import serial
import time
from datetime import datetime
from threading import Thread, Event


class TimerThreadWrite(Thread):
    def __init__(self, event, bus, interval=0.05):
        Thread.__init__(self)
        self.stopped = event
        self.interval = interval
        self.bus = bus
    
    def run(self):
        # Thread to send messages over I2C
        while not self.stopped.wait(self.interval):
            try:
                now = datetime.now().time() # time object
                self.bus.write(b"Hello from Raspberry Pi! Timestamp: ", now, "\n")
                line = self.bus.readline().decode('utf-8').rstrip() # Read for 'timeout' time [sec] or until all the data is recived
                                                                    # Should add that the thread terminates if the it cant write/read
                print(line) 
            except serial.SerialException or TypeError as e: # Not sure this is allowed
                #There is no new data from serial port
                print("Serial error got ",e)
                self.bus.close()
                self.stopped.set() # This will close the thread

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1) # If the name is not the arduino test '/dev/ttyUSB0' [This is for USB communication! if I2C is used name need to be changed]
    # ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1) // Test out different baud rate to speed communication up
    ser.flush()

    # Start I2C-write thread
    thread_stopped_write = Event()
    thread_write = TimerThreadWrite(thread_stopped_write,ser)
    thread_write.name = 'Write thread'
    thread_write.start()

    thread_write.join() # Join the write thread to main so that main thread will stay active until write thread ends
    ser.close()
    print("Terminating...")
    time.sleep(1)