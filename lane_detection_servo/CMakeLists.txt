cmake_minimum_required(VERSION 3.0.2)
project(lane_detection_servo)

# Find catkin and any other catkin packages
find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  cv_bridge
  sensor_msgs
)

# Declare a catkin package
catkin_package()

# Include directories
include_directories(
  ${catkin_INCLUDE_DIRS}
)

# Install Python scripts
catkin_install_python(PROGRAMS
  src/lane_detection_publisher.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

# Link libraries (Not needed for Python scripts, but can be included if C++ components are added)
# target_link_libraries(lane_detection_publisher
#   ${catkin_LIBRARIES}
# )

