#!/usr/bin/env python3

import rospy
import serial
from geometry_msgs.msg import Twist

class ArduinoInterface:
    def __init__(self):
        rospy.init_node('arduino_interface', anonymous=True)
        
        # Setup serial port
        self.serial_port = serial.Serial('/dev/ttyUSB0', 9600)  # Adjust port as needed
        
        # Subscriber for velocity commands
        self.cmd_sub = rospy.Subscriber('/cmd_vel', Twist, self.cmd_callback)
        
        rospy.loginfo("Arduino Interface node started")

    def cmd_callback(self, msg):
        linear_x = msg.linear.x
        angular_z = msg.angular.z
        
        # Send commands to Arduino (example format)
        command = f"{linear_x},{angular_z}\n"
        self.serial_port.write(command.encode())
        
        rospy.loginfo(f"Sent command: {command.strip()}")

if __name__ == '__main__':
    try:
        ArduinoInterface()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

