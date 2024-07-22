cmake_minimum_required(VERSION 2.8.3)
project(jetracer_bringup)

find_package(catkin REQUIRED COMPONENTS
  rospy
  geometry_msgs
  std_msgs
)

catkin_package()

catkin_install_python(PROGRAMS
  src/cmd_vel_servo.py
  src/racecar.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

