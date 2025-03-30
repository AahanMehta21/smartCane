import haptics
import ultraSonic
import time

fetch_time = 0.4

# Thresholds and corresponding RPM values
thresholds_rpm = [
    {"threshold": 5, "rpm": 25},   # Distance < 5 cm -> RPM 25
    {"threshold": 15, "rpm": 10},  # Distance < 15 cm -> RPM 10
    {"threshold": 25, "rpm": 2},   # Distance < 25 cm -> RPM 2
]

try:
    while True:
        dist = ultraSonic.measure_distance()

        if dist is None:
            print("Measurement failed")
            continue
        
        # Loop through the thresholds and set the RPM accordingly
        for threshold_rpm in thresholds_rpm:
            if dist < threshold_rpm["threshold"]:
                haptics.stepper_rotate(rpm=threshold_rpm["rpm"], duration=fetch_time)
                break  # Exit the loop after applying the first matching threshold
        
        time.sleep(fetch_time)  # Wait before next cycle

except KeyboardInterrupt:
    print("Stopped by user")
    GPIO.cleanup()  # Cleanup GPIO on exit
