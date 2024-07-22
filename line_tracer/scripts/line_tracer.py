#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist
import cv2
import numpy as np

class LineTracer:
    def __init__(self):
        rospy.init_node('line_tracing_node')
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.rate = rospy.Rate(10)  # 10 Hz

      
        self.cap = cv2.VideoCapture(0)

    def gray(self, image):
        return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    def gauss(self, image):
        return cv2.GaussianBlur(image, (5, 5), 0)

    def canny(self, image, p1, p2):
        return cv2.Canny(image, p1, p2)

    def region(self, image):
        height, width = image.shape
        triangle = np.array([
            [(100, height), (475, 325), (width, height)]
        ])
        mask = np.zeros_like(image)
        mask = cv2.fillPoly(mask, triangle, 255)
        mask = cv2.bitwise_and(image, mask)
        return mask

    def make_points(self, image, average):
        slope, y_int = average
        y1 = image.shape[0]
        y2 = int(y1 * (3/5))
        x1 = int((y1 - y_int) // slope)
        x2 = int((y2 - y_int) // slope)
        return np.array([x1, y1, x2, y2])

    def average(self, image, lines):
        left = []
        right = []
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            parameters = np.polyfit((x1, x2), (y1, y2), 1)
            slope = parameters[0]
            y_int = parameters[1]
            if slope < 0:
                left.append((slope, y_int))
            else:
                right.append((slope, y_int))
        if left:
            left_avg = np.average(left, axis=0)
            left_line = self.make_points(image, left_avg)
        else:
            left_line = None
        if right:
            right_avg = np.average(right, axis=0)
            right_line = self.make_points(image, right_avg)
        else:
            right_line = None
        return left_line, right_line

    def display_lines(self, image, lines):
        lines_image = np.zeros_like(image)
        if lines is not None:
            for line in lines:
                if line is not None:
                    x1, y1, x2, y2 = line
                    cv2.line(lines_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
        return lines_image

    def run(self):
        while not rospy.is_shutdown():
            try:
                ret, frame = self.cap.read()
                if not ret:
                    rospy.logerr("Failed to capture image")
                    continue
                
                copy = np.copy(frame)
                gray_img = self.gray(copy)
                gaus_img = self.gauss(gray_img)
                edges = self.canny(gaus_img, 50, 150)
                isolated = self.region(edges)
                
                lines = cv2.HoughLinesP(isolated, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
                
                if lines is not None:
                    averaged_lines = self.average(copy, lines)
                    black_lines = self.display_lines(copy, averaged_lines)
                    lanes = cv2.addWeighted(copy, 0.8, black_lines, 1, 1)
                else:
                    lanes = copy

                # 
                cmd_vel = Twist()
                cmd_vel.linear.x = 0.05  # 

                if averaged_lines[0] is not None and averaged_lines[1] is not None:
                    
                    left_line = averaged_lines[0]
                    right_line = averaged_lines[1]
                    mid = (left_line[2] + right_line[2]) // 2
                    frame_mid = frame.shape[1] // 2
                    deviation = frame_mid - mid
                    cmd_vel.angular.z = -deviation / 100.0
                else:
                    cmd_vel.angular.z = 0  

                self.pub.publish(cmd_vel)
                rospy.loginfo(f"Linear: {cmd_vel.linear.x}, Angular: {cmd_vel.angular.z}")

                cv2.imshow('Lanes', lanes)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                self.rate.sleep()

            except Exception as e:
                rospy.logerr(f"Error: {e}")

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    node = LineTracer()
    node.run()

