#!/usr/bin/env python3

import rospy
import numpy as np
import json
from sensor_msgs.msg import CameraInfo
from cv_bridge import CvBridge

class CameraCalibration:
    def __init__(self):
        rospy.init_node('camera_calibration', anonymous=True)
        
        # Load camera calibration parameters
        self.camera_params = self.load_camera_params()
        
        # Subscribe to the camera info topic
        self.camera_info_sub = rospy.Subscriber('/camera/camera_info', CameraInfo, self.camera_info_callback)
        
        self.bridge = CvBridge()
        
        rospy.loginfo("Camera Calibration node started")
    
    def load_camera_params(self):
        # Load camera parameters from a JSON file or similar
        params_file = rospy.get_param('~camera_params_file', 'camera_params.json')
        try:
            with open(params_file, 'r') as f:
                params = json.load(f)
            return params
        except Exception as e:
            rospy.logerr(f"Failed to load camera parameters: {e}")
            return None
    
    def camera_info_callback(self, msg):
        if self.camera_params:
            # Apply calibration parameters (example code)
            K = np.array(self.camera_params['K']).reshape((3, 3))
            D = np.array(self.camera_params['D'])
            
            # Example usage
            rospy.loginfo(f"Camera Calibration Parameters: K={K}, D={D}")

if __name__ == '__main__':
    try:
        CameraCalibration()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

