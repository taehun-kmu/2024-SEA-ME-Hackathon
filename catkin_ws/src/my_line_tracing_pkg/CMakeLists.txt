cmake_minimum_required(VERSION 3.0.2)
project(my_line_tracing_pkg)

find_package(catkin REQUIRED COMPONENTS
  rospy
  sensor_msgs
  cv_bridge
)

catkin_package()

include_directories(
  ${catkin_INCLUDE_DIRS}
)

catkin_install_python(PROGRAMS
  src/line_tracing_node.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

