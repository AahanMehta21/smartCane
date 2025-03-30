import RPi.GPIO as GPIO
import time

# GPIO Pins for ULN2003 (IN1 to IN4)
IN1 = 17  # GPIO17 (Pin 11)
IN2 = 18  # GPIO18 (Pin 12)
IN3 = 27  # GPIO27 (Pin 13)
IN4 = 22  # GPIO22 (Pin 15)

# Full-step sequence for stepper motor
step_sequence = [
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1]
]

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setup([IN1, IN2, IN3, IN4], GPIO.OUT)

def stepper_rotate(rpm=10, duration=5):
    """
    Rotate the stepper motor at a given RPM for a specific duration.
    
    :param rpm: Rotations Per Minute (default: 10)
    :param duration: Duration to run the motor in seconds (default: 5)
    :param direction: 1 for clockwise, -1 for counterclockwise
    """
    steps_per_revolution = 512  # Full revolution for 28BYJ-48
    total_steps = int((rpm / 60) * steps_per_revolution * duration)
    step_delay = 60 / (rpm * steps_per_revolution)  # Delay per step
    
    start_time = time.time()
    
    while time.time() - start_time < duration:  # Run for the given duration
        for step in step_sequence:
            GPIO.output(IN1, step[0])
            GPIO.output(IN2, step[1])
            GPIO.output(IN3, step[2])
            GPIO.output(IN4, step[3])
            time.sleep(step_delay)  # Control speed

