cmake_minimum_required(VERSION 3.8)
project(devotics_arm_description)

find_package(ament_cmake REQUIRED)

# Install resource directories to package share
install(
  DIRECTORY launch rviz urdf
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
