#!/usr/bin/env python3

import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge, CvBridgeError

class SignalDetectionNode:
    def __init__(self):
        rospy.init_node('signal_detection_node', anonymous=True)
        
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber('/camera/image_raw', Image, self.image_callback)
        self.cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        
        self.twist = Twist()

    def image_callback(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except CvBridgeError as e:
            rospy.logerr(f'CvBridge Error: {e}')
            return
        
        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        red_lower = np.array([0, 50, 50])
        red_upper = np.array([10, 255, 255])
        yellow_lower = np.array([20, 100, 100])
        yellow_upper = np.array([30, 255, 255])
        green_lower = np.array([35, 100, 100])
        green_upper = np.array([85, 255, 255])
        
        red_mask = cv2.inRange(hsv, red_lower, red_upper)
        yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
        green_mask = cv2.inRange(hsv, green_lower, green_upper)
        
        if cv2.countNonZero(red_mask) > 500:
            self.twist.linear.x = 0.0
            rospy.loginfo("Red light detected")
        elif cv2.countNonZero(yellow_mask) > 500:
            self.twist.linear.x = 0.0
            rospy.loginfo("Yellow light detected")
        elif cv2.countNonZero(green_mask) > 500:
            self.twist.linear.x = 0.2
            rospy.loginfo("Green light detected")
        else:
            self.twist.linear.x = 0.2
        
        self.cmd_pub.publish(self.twist)

if __name__ == '__main__':
    try:
        SignalDetectionNode()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

