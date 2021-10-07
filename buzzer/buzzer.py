import RPi.GPIO as GPIO
import time

buzzer_pin = 27


def buzz(frequency, length):  # create the function "buzz" and feed it the pitch and duration)
    if (frequency == 0):
        time.sleep(length)
        return
    period = 1.0 / frequency  # in physics, the period (sec/cyc) is the inverse of the frequency (cyc/sec)
    delayValue = period / 2  # calculate the time for half of the wave
    numCycles = int(length * frequency)  # the number of waves to produce is the duration times the frequency

    for i in range(numCycles):  # start a loop from 0 to the variable "cycles" calculated above
        GPIO.output(buzzer_pin, True)  # set pin 27 to high
        time.sleep(delayValue)  # wait with pin 27 high
        GPIO.output(buzzer_pin, False)  # set pin 27 to low
        time.sleep(delayValue)  # wait with pin 27 low

def play_notes(notes):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzzer_pin, GPIO.IN)
    GPIO.setup(buzzer_pin, GPIO.OUT)
    for frequency, length in notes:
        buzz(frequency, length)

    GPIO.cleanup()

def thinking_noise():
    play_notes([(300, 0.2), (0, 0.2)] * 3)

def happy_noise():
    play_notes([(440, 0.25), (660, 0.25)])

def sad_noise():
    play_notes([(440, 0.25), (370, 0.25)])