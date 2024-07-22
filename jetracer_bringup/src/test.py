#!/usr/bin/env python3
import rospy
from adafruit_servokit import ServoKit


i2c_address = 0x40
steering_channel = 0
throttle_channel = 1


rospy.init_node('servo_test')
kit = ServoKit(channels=16, address=i2c_address)
steering_motor = kit.continuous_servo[steering_channel]
throttle_motor = kit.continuous_servo[throttle_channel]


def test_servos():
    try:
        while not rospy.is_shutdown():
            steering_motor.throttle = 1
            throttle_motor.throttle = 1
            rospy.sleep(2)
            steering_motor.throttle = -1
            throttle_motor.throttle = -1
            rospy.sleep(2)
    except rospy.ROSInterruptException:
        pass
    finally:
        steering_motor.throttle = 0
        throttle_motor.throttle = 0

if __name__ == '__main__':
    test_servos()
