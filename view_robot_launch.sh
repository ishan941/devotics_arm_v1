#!/usr/bin/env bash
cd /home/ishan/devotics_arm_v1_ws/src/devotics_arm_v1 || exit 1
colcon build --packages-select devotics_arm_description --allow-overriding devotics_arm_description
source /home/ishan/devotics_arm_v1_ws/src/devotics_arm_v1/install/setup.bash
ros2 launch devotics_arm_description view_robot.launch.py
