cmake_minimum_required(VERSION 3.0.2)
project(rim_track2)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  sensor_msgs
  cv_bridge
  image_transport
  dynamic_reconfigure
)

catkin_python_setup()

catkin_package(
  CATKIN_DEPENDS rospy std_msgs sensor_msgs cv_bridge image_transport dynamic_reconfigure
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

# Install Python scripts
catkin_install_python(PROGRAMS
  src/line_detection_node.py
  src/obstacle_detection_node.py
  src/signal_detection_node.py
  src/main.py
  scripts/arduino_interface.py
  scripts/camera_calibration.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

