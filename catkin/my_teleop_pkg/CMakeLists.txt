cmake_minimum_required(VERSION 2.8.3)
project(my_teleop_pkg)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  geometry_msgs
  sensor_msgs
)

catkin_package(
  CATKIN_DEPENDS rospy std_msgs geometry_msgs sensor_msgs
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

catkin_install_python(PROGRAMS
  src/teleop_node.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

