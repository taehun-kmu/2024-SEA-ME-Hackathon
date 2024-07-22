#!/usr/bin/env python3

import cv2
import numpy as np
import rospy
from std_msgs.msg import Float32

# Image preprocessing functions
def gray(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def gauss(image):
    return cv2.GaussianBlur(image, (5, 5), 0)

def canny(image, p1, p2):
    return cv2.Canny(image, p1, p2)

def region(image):
    height, width = image.shape
    triangle = np.array([
        [(100, height), (475, 325), (width, height)]
    ])
    mask = np.zeros_like(image)
    mask = cv2.fillPoly(mask, triangle, 255)
    mask = cv2.bitwise_and(image, mask)
    return mask

def make_points(image, average):
    slope, y_int = average
    y1 = image.shape[0]
    y2 = int(y1 * (3 / 5))
    x1 = int((y1 - y_int) // slope)
    x2 = int((y2 - y_int) // slope)
    return np.array([x1, y1, x2, y2])

def average(image, lines):
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
    if len(left) > 0:
        left_avg = np.average(left, axis=0)
        left_line = make_points(image, left_avg)
    else:
        left_line = np.array([0, 0, 0, 0])
    if len(right) > 0:
        right_avg = np.average(right, axis=0)
        right_line = make_points(image, right_avg)
    else:
        right_line = np.array([0, 0, 0, 0])
    return np.array([left_line, right_line])

def display_lines(image, lines):
    lines_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line
            cv2.line(lines_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return lines_image

def calculate_steering_angle(averaged_lines, frame_width):
    if averaged_lines is None:
        return 0
    
    left_line, right_line = averaged_lines

    # Calculate the center of the lane
    if left_line[0] != 0 and right_line[0] != 0:
        x1_left, y1_left, x2_left, y2_left = left_line
        x1_right, y1_right, x2_right, y2_right = right_line
        center_x = (x1_left + x2_left + x1_right + x2_right) // 4
    else:
        center_x = frame_width // 2
    
    # Calculate the deviation from the center
    error = frame_width // 2 - center_x

    # Generate control signal (proportional control)
    steering_angle = -error / (frame_width // 2) * 30  # 30 is the range of steering angles.

    return steering_angle

def main():
    rospy.init_node('lane_detection_publisher', anonymous=False)
    steering_pub = rospy.Publisher('/Steering', Float32, queue_size=10)
    
    cap = cv2.VideoCapture(0)  # Capture video from USB camera

    while not rospy.is_shutdown():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Image preprocessing
        gray_frame = gray(frame)
        blurred_frame = gauss(gray_frame)
        edges = canny(blurred_frame, 50, 150)
        masked_edges = region(edges)

        # Detect lines using Hough transform
        lines = cv2.HoughLinesP(masked_edges, 2, np.pi / 180, 100, np.array([]), minLineLength=40, maxLineGap=5)

        # Average and draw lines
        averaged_lines = average(frame, lines)
        black_lines = display_lines(frame, averaged_lines)
        lanes = cv2.addWeighted(frame, 0.8, black_lines, 1, 1)

        # Driving control
        steering_angle = calculate_steering_angle(averaged_lines, frame.shape[1])
        rospy.loginfo(f"Steering Angle: {steering_angle:.2f}")
        
        # Publish the steering angle
        steering_pub.publish(Float32(steering_angle))

        # Display video
        cv2.imshow("Lane Detection", lanes)

        # Exit when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

