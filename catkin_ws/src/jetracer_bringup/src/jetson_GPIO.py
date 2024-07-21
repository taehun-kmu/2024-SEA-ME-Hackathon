import Jetson.GPIO as GPIO
import time


GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.IN)

try:
    while True:

        pin_status = GPIO.input(12)

        print(f"GPIO 12 상태: {pin_status}")
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()

