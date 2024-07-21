#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from adafruit_servokit import ServoKit
import traitlets

class NvidiaRacecar(traitlets.HasTraits):
    i2c_address = traitlets.Integer(default_value=0x40)
    steering_gain = traitlets.Float(default_value=-0.65)
    steering_offset = traitlets.Float(default_value=0)
    steering_channel = traitlets.Integer(default_value=0)
    throttle_gain = traitlets.Float(default_value=0.8)
    throttle_channel = traitlets.Integer(default_value=1)

    def __init__(self, *args, **kwargs):
        super(NvidiaRacecar, self).__init__(*args, **kwargs)
        self.kit = ServoKit(channels=16, address=self.i2c_address)
        self.kit._pca.frequency = 60
        self.steering_motor = self.kit.continuous_servo[self.steering_channel]
        self.throttle_motor = self.kit.continuous_servo[self.throttle_channel]
        self.steering_motor.throttle = 0
        self.throttle_motor.throttle = 0

        rospy.init_node('nvidia_racecar')
        rospy.Subscriber('/cmd_vel', Twist, self.cmd_vel_callback)

    def cmd_vel_callback(self, msg):
        # Convert cmd_vel to servo control values
        linear = msg.linear.x
        angular = msg.angular.z

        # Calculate steering and throttle values
        steering_value = angular * self.steering_gain + self.steering_offset
        throttle_value = linear * self.throttle_gain

        # Set values to traitlets (automatically updates servo motors)
        self.steering_motor.throttle = steering_value
        self.throttle_motor.throttle = throttle_value

        rospy.loginfo(f"Received cmd_vel: linear={linear}, angular={angular}, "
                      f"steering={steering_value}, throttle={throttle_value}")

if __name__ == '__main__':
    racecar = NvidiaRacecar()
    rospy.spin()

