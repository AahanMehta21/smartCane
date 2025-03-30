import RPi.GPIO as GPIO
import time

TRIG = 23  # Trigger pin
ECHO = 24  # Echo pin

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def measure_distance():
    # Send a short pulse to trigger the sensor
    GPIO.output(TRIG, True)
    time.sleep(0.00001)  # 10µs pulse
    GPIO.output(TRIG, False)

    pulse_start = time.monotonic()
    timeout = pulse_start + 1  # 1-second timeout for safety

    # Wait for the echo to start, with a timeout
    while GPIO.input(ECHO) == 0:
        pulse_start = time.monotonic()
        if pulse_start > timeout:
            print("Echo signal not received (start)")
            return None  # No response

    pulse_end = time.monotonic()
    timeout = pulse_end + 1 

    # Wait for the echo to end, with a timeout
    while GPIO.input(ECHO) == 1:
        pulse_end = time.monotonic()
        if pulse_end > timeout:
            print("Echo signal not received (end)")
            return None  # No response

    # Calculate the duration and convert to distance
    pulse_duration = pulse_end - pulse_start
    distance = (pulse_duration * 34300) / 2  # Speed of sound = 343 m/s

    return distance
