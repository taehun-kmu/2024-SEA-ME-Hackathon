#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
import serial

class TeleopNode:
    def __init__(self):
        rospy.init_node('teleop_node')

        self.ser = serial.Serial('/dev/ttyTHS1', 9600, timeout=1)

        self.pub_cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        rospy.Subscriber('/joy', Joy, self.joy_callback)

        self.max_linear_speed = 1.0
        self.max_angular_speed = 1.0

    def set_wheel_velocity(self, l_vel, r_vel):
        self.ser.write('$cVW,{:.0f},{:.0f}\n'.format(l_vel, r_vel).encode())

    def joy_callback(self, msg):
        if msg.buttons[0] == 1:
            self.set_wheel_velocity(0.0, 0.0)
            rospy.loginfo("stop")
        elif msg.buttons[1] == 1:
            self.set_wheel_velocity(0.5, -0.5)
            rospy.loginfo("turn right")
        elif msg.buttons[2] == 1:
            self.set_wheel_velocity(1.0, -1.0)
            rospy.loginfo("turn round")
        else:
            linear = msg.axes[1] * self.max_linear_speed
            angular = msg.axes[0] * self.max_angular_speed
            l_vel = linear - angular
            r_vel = linear + angular
            self.set_wheel_velocity(l_vel, r_vel)
            rospy.loginfo("input joystick: linear={}, angular={}".format(linear, angular))

            # Publish cmd_vel to NvidiaRacecar
            cmd_vel = Twist()
            cmd_vel.linear.x = linear
            cmd_vel.angular.z = angular
            self.pub_cmd_vel.publish(cmd_vel)

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    teleop_node = TeleopNode()
    teleop_node.run()

