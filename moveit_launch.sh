#!/usr/bin/env bash
cd /home/ishan/devotics_arm_v1_ws/src/devotics_arm_v1 || exit 1
source /opt/ros/jazzy/setup.bash
colcon build --packages-select devotics_arm_description devotics_arm_moveit_config --allow-overriding devotics_arm_description devotics_arm_moveit_config
source /home/ishan/devotics_arm_v1_ws/src/devotics_arm_v1/install/setup.bash
ros2 launch devotics_arm_moveit_config demo.launch.py
