#!/usr/bin/env python3

import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge, CvBridgeError

class LineDetectionNode:
    def __init__(self):
        rospy.init_node('line_detection_node', anonymous=True)
        
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
        
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        
        # Find contours
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest_contour)
            if M['m00'] != 0:
                cx = int(M['m10'] / M['m00'])
                cv2.drawContours(cv_image, [largest_contour], -1, (0, 255, 0), 3)
                
                # Control logic for line following
                if cx < cv_image.shape[1] // 3:
                    self.twist.angular.z = 0.5
                    self.twist.linear.x = 0.1
                elif cx > 2 * cv_image.shape[1] // 3:
                    self.twist.angular.z = -0.5
                    self.twist.linear.x = 0.1
                else:
                    self.twist.angular.z = 0
                    self.twist.linear.x = 0.2

                self.cmd_pub.publish(self.twist)
        
        cv2.imshow("Line Detection", cv_image)
        cv2.waitKey(3)

if __name__ == '__main__':
    try:
        LineDetectionNode()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

