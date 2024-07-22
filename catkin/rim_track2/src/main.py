#!/usr/bin/env python3

import rospy
import subprocess

def start_nodes():
    # Start the line detection node
    rospy.loginfo("Starting line_detection_node")
    subprocess.Popen(['rosrun', 'rim_track2', 'line_detection_node.py'])

    # Start the obstacle detection node
    rospy.loginfo("Starting obstacle_detection_node")
    subprocess.Popen(['rosrun', 'rim_track2', 'obstacle_detection_node.py'])

    # Start the signal detection node
    rospy.loginfo("Starting signal_detection_node")
    subprocess.Popen(['rosrun', 'rim_track2', 'signal_detection_node.py'])

    # Start the Arduino interface node
    rospy.loginfo("Starting arduino_interface_node")
    subprocess.Popen(['rosrun', 'rim_track2', 'arduino_interface.py'])

    rospy.loginfo("All nodes started")

if __name__ == '__main__':
    try:
        rospy.init_node('main_node', anonymous=True)
        start_nodes()
        rospy.spin()  # Keep the node running
    except rospy.ROSInterruptException:
        pass

