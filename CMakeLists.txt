cmake_minimum_required(VERSION 3.8)
project(my_robot_launch)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)

# Install launch directory
install(DIRECTORY launch/
  DESTINATION share/${PROJECT_NAME}/launch
)

# Install rviz directory
install(DIRECTORY rviz/
  DESTINATION share/${PROJECT_NAME}/rviz
)

ament_package()