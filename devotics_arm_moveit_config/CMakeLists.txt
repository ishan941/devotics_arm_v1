cmake_minimum_required(VERSION 3.22)
project(devotics_arm_moveit_config)

find_package(ament_cmake REQUIRED)

if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/launch")
  install(
    DIRECTORY launch
    DESTINATION share/${PROJECT_NAME}
  )
endif()

install(DIRECTORY config DESTINATION share/${PROJECT_NAME})
install(FILES .setup_assistant DESTINATION share/${PROJECT_NAME})

install(
  PROGRAMS
    scripts/pick_and_place.py
    scripts/esp32_bridge.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
