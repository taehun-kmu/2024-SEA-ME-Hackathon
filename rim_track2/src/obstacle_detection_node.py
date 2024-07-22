#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class ObstacleDetectionNode:
    def __init__(self):
        rospy.init_node('obstacle_detection_node', anonymous=True)
        
        self.laser_sub = rospy.Subscriber('/scan', LaserScan, self.laser_callback)
        self.cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        
        self.twist = Twist()

    def laser_callback(self, data):
        ranges = data.ranges
        min_distance = min(ranges)
        
        if min_distance < 1.0:
            self.twist.linear.x = 0.0
            self.twist.angular.z = 0.5
        else:
            self.twist.linear.x = 0.2
            self.twist.angular.z = 0.0
        
        self.cmd_pub.publish(self.twist)

if __name__ == '__main__':
    try:
        ObstacleDetectionNode()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

