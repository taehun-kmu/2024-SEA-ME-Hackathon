#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist, PoseStamped
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np
from dynamic_reconfigure.server import Server
from rim_line.cfg import PIDConfig

class LineTracer:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.previous_error = 0
        self.integral = 0

    def pid_control(self, error):
        self.integral += error
        derivative = error - self.previous_error
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.previous_error = error
        return output

class LineFollower:
    def __init__(self):
        rospy.init_node('line_follower')
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.bridge = CvBridge()
        rospy.Subscriber('/camera/rgb/image_raw', Image, self.image_callback)
        rospy.Subscriber('/slam/pose', PoseStamped, self.pose_callback)
        self.line_tracer = LineTracer(0.1, 0.01, 0.05)
        self.srv = Server(PIDConfig, self.reconfigure_callback)
        self.current_pose = None

    def reconfigure_callback(self, config, level):
        self.line_tracer.kp = config.kp
        self.line_tracer.ki = config.ki
        self.line_tracer.kd = config.kd
        return config

    def pose_callback(self, msg):
        self.current_pose = msg.pose.position

    def image_callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        
        lower_white = np.array([0, 0, 200])
        upper_white = np.array([180, 50, 255])
        white_mask = cv2.inRange(hsv, lower_white, upper_white)
        
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])
        yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        mask = cv2.bitwise_or(white_mask, yellow_mask)
        blurred = cv2.GaussianBlur(mask, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)

        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, minLineLength=50, maxLineGap=10)
        if lines is not None:
            line_center_sum = 0
            count = 0
            
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(cv_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                line_center = (x1 + x2) // 2
                line_center_sum += line_center
                count += 1
            
            if count > 0:
                average_line_center = line_center_sum // count
                image_center = cv_image.shape[1] // 2
                error = image_center - average_line_center
                
                control = self.line_tracer.pid_control(error)
                twist = Twist()
                twist.linear.x = 0.3
                twist.angular.z = control
                self.cmd_vel_pub.publish(twist)

        cv_image = cv2.resize(cv_image, (640, 480))
        cv2.imshow('Frame', cv_image)
        cv2.waitKey(1)

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    follower = LineFollower()
    follower.run()

