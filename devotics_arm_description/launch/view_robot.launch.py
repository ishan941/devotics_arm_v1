import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg_share = FindPackageShare('devotics_arm_description')

    default_model_path = PathJoinSubstitution(
        [pkg_share, 'urdf', 'devotics_arm_v1.urdf.xacro']
    )
    default_rviz_config_path = PathJoinSubstitution(
        [pkg_share, 'rviz', 'view_robot.rviz']
    )

    use_gui = LaunchConfiguration('use_gui')
    use_rviz = LaunchConfiguration('use_rviz')

    # Convert Xacro -> URDF string parameter
    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name='xacro')]),
            ' ',
            LaunchConfiguration('model'),
        ]
    )

    # In ROS 2 Jazzy, string parameters from Command must be wrapped in ParameterValue
    robot_description = {
        'robot_description': ParameterValue(robot_description_content, value_type=str)
    }

    # 1. Publishes 3D TF transforms from joint states and URDF
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='both',
        parameters=[robot_description],
    )

    # 2. Provides the GUI slider window to rotate joints
    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        output='screen',
        condition=IfCondition(use_gui),
    )

    # 3. 3D Visualizer
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='log',
        arguments=['-d', LaunchConfiguration('rvizconfig')],
        condition=IfCondition(use_rviz),
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                name='use_gui',
                default_value='true',
                description='Flag to enable joint_state_publisher_gui',
            ),
            DeclareLaunchArgument(
                name='use_rviz',
                default_value='true',
                description='Flag to start RViz2',
            ),
            DeclareLaunchArgument(
                name='model',
                default_value=default_model_path,
                description='Absolute path to robot xacro/urdf file',
            ),
            DeclareLaunchArgument(
                name='rvizconfig',
                default_value=default_rviz_config_path,
                description='Absolute path to rviz config file',
            ),
            robot_state_publisher_node,
            joint_state_publisher_gui_node,
            rviz_node,
        ]
    )
