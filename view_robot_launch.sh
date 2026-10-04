colcon build --packages-select devotics_arm_description --allow-overriding devotics_arm_description
source install/setup.bash
ros2 launch devotics_arm_description view_robot.launch.py
