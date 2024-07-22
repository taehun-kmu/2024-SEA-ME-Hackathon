cmake_minimum_required(VERSION 3.0.2)
project(jetracer_teleop)

find_package(catkin REQUIRED COMPONENTS
  rospy
  geometry_msgs
  sensor_msgs
  std_msgs
)

catkin_package()

include_directories(
  ${catkin_INCLUDE_DIRS}
)

catkin_install_python(PROGRAMS
  src/teleop_node.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

