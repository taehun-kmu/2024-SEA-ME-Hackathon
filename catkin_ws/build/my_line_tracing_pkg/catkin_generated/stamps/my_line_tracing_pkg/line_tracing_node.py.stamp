#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import camera_utils
import cv2

class LineTracer:
    def __init__(self):
        rospy.init_node('line_tracing_node')
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.rate = rospy.Rate(10)

    def run(self):
        while not rospy.is_shutdown():
            try:
                frame = camera_utils.get_frame_from_camera()
                steering_angle, processed_frame = camera_utils.process_frame(frame)

                cmd_vel = Twist()
                cmd_vel.angular.z = steering_angle
                cmd_vel.linear.x = 0.1
                self.pub.publish(cmd_vel)

                rospy.loginfo(f"Steering Angle: {steering_angle}")

                # Display the processed frame
                cv2.imshow('Processed Frame', processed_frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                self.rate.sleep()

            except Exception as e:
                rospy.logerr(f"Error: {e}")

        cv2.destroyAllWindows()

if __name__ == '__main__':
    node = LineTracer()
    node.run()

