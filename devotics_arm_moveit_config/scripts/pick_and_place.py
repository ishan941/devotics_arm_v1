#!/usr/bin/env python3
"""
Devotics Arm V1 — Autonomous Pick & Place Mission Node
Executes a complete 5-DOF + Gripper Pick-and-Place trajectory via MoveIt 2 /
ros2_control FollowJointTrajectory action servers and visualizes a 3D target object
in RViz.
"""

import argparse
import time
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint
from visualization_msgs.msg import Marker
from builtin_interfaces.msg import Duration


class DevoticsV1PickAndPlace(Node):
    def __init__(self):
        super().__init__('devotics_v1_pick_and_place')

        self.arm_client = ActionClient(
            self,
            FollowJointTrajectory,
            '/devotics_arm_controller/follow_joint_trajectory',
        )
        self.gripper_client = ActionClient(
            self,
            FollowJointTrajectory,
            '/gripper_controller/follow_joint_trajectory',
        )
        self.marker_pub = self.create_publisher(Marker, '/visualization_marker', 10)

        self.arm_joints = [
            'joint_1',
            'joint_2',
            'joint_3',
            'joint_4',
            'joint_5',
        ]
        self.gripper_joints = [
            'gripper_left_finger_joint',
            'gripper_right_finger_joint',
        ]

        # Exact TCP world coordinates for Pick & Place stations
        self.pick_xyz = (-0.220, 0.130, 0.071)
        self.place_xyz = (-0.215, -0.137, 0.071)

        self.get_logger().info('Waiting for MoveIt 2 / ros2_control trajectory servers...')
        self.arm_client.wait_for_server()
        self.gripper_client.wait_for_server()
        self.get_logger().info('Connected to arm & gripper controllers!')

    def publish_object_marker(self, frame_id: str, xyz: tuple, grasped: bool = False):
        """Publishes the 3D target cube in RViz (either on the table or attached to tool0)."""
        marker = Marker()
        marker.header.frame_id = frame_id
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = 'pick_place_cube'
        marker.id = 1
        marker.type = Marker.CUBE
        marker.action = Marker.ADD

        marker.pose.position.x = float(xyz[0])
        marker.pose.position.y = float(xyz[1])
        marker.pose.position.z = float(xyz[2])
        marker.pose.orientation.w = 1.0

        marker.scale.x = 0.026
        marker.scale.y = 0.026
        marker.scale.z = 0.026

        if grasped:
            marker.color.r = 0.95
            marker.color.g = 0.45
            marker.color.b = 0.10
            marker.color.a = 0.95
        else:
            marker.color.r = 0.15
            marker.color.g = 0.85
            marker.color.b = 0.30
            marker.color.a = 0.95

        self.marker_pub.publish(marker)

    def move_arm(self, label: str, positions: list, duration_sec: float = 2.5) -> bool:
        goal_msg = FollowJointTrajectory.Goal()
        goal_msg.trajectory.joint_names = self.arm_joints

        point = JointTrajectoryPoint()
        point.positions = [float(p) for p in positions]
        sec = int(duration_sec)
        nanosec = int((duration_sec - sec) * 1e9)
        point.time_from_start = Duration(sec=sec, nanosec=nanosec)
        goal_msg.trajectory.points.append(point)

        self.get_logger().info(f'[{label}] Moving arm -> {positions} ({duration_sec:.1f}s)')
        send_future = self.arm_client.send_goal_async(goal_msg)
        rclpy.spin_until_future_complete(self, send_future)

        goal_handle = send_future.result()
        if not goal_handle or not goal_handle.accepted:
            self.get_logger().error(f'[{label}] Arm trajectory rejected!')
            return False

        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)
        return True

    def move_gripper(self, label: str, opening: float, duration_sec: float = 1.0) -> bool:
        goal_msg = FollowJointTrajectory.Goal()
        goal_msg.trajectory.joint_names = self.gripper_joints

        point = JointTrajectoryPoint()
        point.positions = [float(opening), float(opening)]
        sec = int(duration_sec)
        nanosec = int((duration_sec - sec) * 1e9)
        point.time_from_start = Duration(sec=sec, nanosec=nanosec)
        goal_msg.trajectory.points.append(point)

        self.get_logger().info(f'[{label}] Gripper -> {opening:.4f} m')
        send_future = self.gripper_client.send_goal_async(goal_msg)
        rclpy.spin_until_future_complete(self, send_future)

        goal_handle = send_future.result()
        if not goal_handle or not goal_handle.accepted:
            self.get_logger().error(f'[{label}] Gripper command rejected!')
            return False

        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)
        return True

    def run_cycle(self):
        # Joint Poses: [joint_1, joint_2, joint_3, joint_4, joint_5]
        HOME = [0.0, 0.0, 0.0, 0.0, 0.0]
        READY = [0.0, -0.20, -0.15, 0.20, 0.0]
        PICK_APPROACH = [-0.55, -0.25, -0.25, 0.15, 0.0]
        PICK_POSE = [-0.55, -0.55, -0.50, 0.35, 0.0]
        PLACE_APPROACH = [0.55, -0.25, -0.25, 0.15, 0.0]
        PLACE_POSE = [0.55, -0.55, -0.50, 0.35, 0.0]

        GRIPPER_OPEN = 0.012
        GRIPPER_CLOSED = -0.004

        # Spawn object at Pick station
        for _ in range(3):
            self.publish_object_marker('world', self.pick_xyz, grasped=False)
            time.sleep(0.1)

        # 1. Move to Ready & Open Gripper
        self.move_arm('1/9 READY', READY, duration_sec=2.0)
        self.move_gripper('2/9 OPEN GRIPPER', GRIPPER_OPEN, duration_sec=1.0)

        # 2. Approach Pick Station
        self.move_arm('3/9 PICK APPROACH', PICK_APPROACH, duration_sec=2.2)

        # 3. Descend to Pick Pose
        self.move_arm('4/9 DESCEND TO PICK', PICK_POSE, duration_sec=1.8)
        time.sleep(0.3)

        # 4. Grasp Object & Attach Marker to tool0
        self.move_gripper('5/9 GRASP OBJECT', GRIPPER_CLOSED, duration_sec=1.0)
        self.publish_object_marker('tool0', (0.0, 0.0, 0.0), grasped=True)
        time.sleep(0.4)

        # 5. Lift Object
        self.move_arm('6/9 LIFT OBJECT', PICK_APPROACH, duration_sec=1.8)
        self.publish_object_marker('tool0', (0.0, 0.0, 0.0), grasped=True)

        # 6. Swing Across to Place Station
        self.move_arm('7/9 SWING TO PLACE', PLACE_APPROACH, duration_sec=2.8)
        self.publish_object_marker('tool0', (0.0, 0.0, 0.0), grasped=True)

        # 7. Descend to Place Pose
        self.move_arm('8/9 DESCEND TO PLACE', PLACE_POSE, duration_sec=1.8)
        time.sleep(0.3)

        # 8. Release Object at Place Station
        self.move_gripper('9/9 RELEASE OBJECT', GRIPPER_OPEN, duration_sec=1.0)
        self.publish_object_marker('world', self.place_xyz, grasped=False)
        time.sleep(0.4)

        # 9. Retract & Return Home
        self.move_arm('RETRACT', PLACE_APPROACH, duration_sec=1.8)
        self.move_gripper('NEUTRAL GRIPPER', 0.0, duration_sec=1.0)
        self.move_arm('HOME', HOME, duration_sec=2.2)
        self.get_logger().info('Pick & Place cycle completed successfully!')


def main(args=None):
    parser = argparse.ArgumentParser(description='Devotics Arm V1 Pick & Place')
    parser.add_argument(
        '--loop',
        action='store_true',
        help='Continuously repeat the pick-and-place mission',
    )
    parsed_args, ros_args = parser.parse_known_args()

    rclpy.init(args=ros_args)
    node = DevoticsV1PickAndPlace()

    try:
        if parsed_args.loop:
            cycle = 1
            while rclpy.ok():
                node.get_logger().info(f'=== Starting Pick & Place Cycle #{cycle} ===')
                node.run_cycle()
                cycle += 1
                time.sleep(1.0)
        else:
            node.run_cycle()
    except KeyboardInterrupt:
        node.get_logger().info('Pick & Place stopped by user.')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
