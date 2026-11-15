#!/usr/bin/env python3
"""
Devotics Arm V1 — Real-Time MoveIt 2 to ESP32 Physical Hardware Bridge

Subscribes to `/joint_states` (published by MoveIt 2 / ros2_control or
joint_state_publisher_gui), converts the 5 arm joint angles + gripper state
into calibrated servo angles (degrees), and streams them to the ESP32 over
USB Serial (`/dev/ttyUSB0`) or Wi-Fi TCP (`socket://IP:8888`).
"""

import argparse
import math
import os
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import serial
from ament_index_python.packages import get_package_share_directory
import yaml


class DevoticsV1ESP32Bridge(Node):
    def __init__(self, port_override=None, dry_run=False):
        super().__init__('devotics_v1_esp32_bridge')
        self.dry_run = dry_run

        # Load default YAML calibration file from package share
        pkg_share = get_package_share_directory('devotics_arm_moveit_config')
        calib_path = os.path.join(pkg_share, 'config', 'esp32_calibration.yaml')
        with open(calib_path, 'r', encoding='utf-8') as fp:
            raw_cfg = yaml.safe_load(fp)['devotics_v1_esp32_bridge']['ros__parameters']

        self.serial_port = port_override or raw_cfg.get('serial_port', '/dev/ttyUSB0')
        self.baud_rate = int(raw_cfg.get('baud_rate', 115200))
        self.rate_hz = float(raw_cfg.get('update_rate_hz', 25.0))

        self.joint_cfg = {
            f'joint_{i}': raw_cfg[f'joint_{i}'] for i in range(1, 6)
        }
        self.gripper_cfg = raw_cfg['gripper']

        # Latest joint states (radians / meters)
        self.latest_positions = {
            'joint_1': 0.0,
            'joint_2': 0.0,
            'joint_3': 0.0,
            'joint_4': 0.0,
            'joint_5': 0.0,
            'gripper_left_finger_joint': 0.0,
        }
        self.last_sent_cmd = None

        # Open Serial or TCP Socket connection
        self.ser = None
        if not self.dry_run:
            self.connect_esp32()
        else:
            self.get_logger().info('Running in --dry-run mode (printing commands without serial port)')

        self.sub = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10,
        )
        self.timer = self.create_timer(1.0 / self.rate_hz, self.stream_to_esp32)

    def connect_esp32(self):
        try:
            self.get_logger().info(f'Connecting to ESP32 on {self.serial_port} @ {self.baud_rate}...')
            if self.serial_port.startswith('socket://'):
                self.ser = serial.serial_for_url(self.serial_port, timeout=1.0)
            else:
                self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=1.0)
            self.get_logger().info(f'Connected to ESP32 on {self.serial_port}!')
        except Exception as exc:
            self.get_logger().warn(
                f'Could not open {self.serial_port}: {exc}. '
                'Running in preview mode (plug in ESP32 or pass --port /dev/ttyUSB0).'
            )
            self.ser = None

    def joint_state_callback(self, msg: JointState):
        for name, pos in zip(msg.name, msg.position):
            if name in self.latest_positions:
                self.latest_positions[name] = float(pos)

    def rad_to_deg(self, joint_name: str, rad: float) -> int:
        cfg = self.joint_cfg[joint_name]
        deg = cfg['servo_home'] + cfg['direction'] * math.degrees(rad) + cfg['offset_deg']
        clamped = max(int(cfg['servo_min']), min(int(cfg['servo_max']), int(round(deg))))
        return clamped

    def gripper_to_deg(self, meters: float) -> int:
        # Map [-0.005 m (closed) .. +0.012 m (open)] to [closed_deg .. open_deg]
        closed_m = -0.004
        open_m = 0.012
        ratio = (meters - closed_m) / (open_m - closed_m)
        ratio = max(0.0, min(1.0, ratio))
        closed_deg = float(self.gripper_cfg['closed_deg'])
        open_deg = float(self.gripper_cfg['open_deg'])
        return int(round(closed_deg + ratio * (open_deg - closed_deg)))

    def stream_to_esp32(self):
        d1 = self.rad_to_deg('joint_1', self.latest_positions['joint_1'])
        d2 = self.rad_to_deg('joint_2', self.latest_positions['joint_2'])
        d3 = self.rad_to_deg('joint_3', self.latest_positions['joint_3'])
        d4 = self.rad_to_deg('joint_4', self.latest_positions['joint_4'])
        d5 = self.rad_to_deg('joint_5', self.latest_positions['joint_5'])
        d6 = self.gripper_to_deg(self.latest_positions['gripper_left_finger_joint'])

        cmd = f'S {d1} {d2} {d3} {d4} {d5} {d6}\n'
        if cmd == self.last_sent_cmd:
            return

        self.last_sent_cmd = cmd
        self.get_logger().info(f'ESP32 TX -> {cmd.strip()}')

        if self.ser and self.ser.is_open:
            try:
                self.ser.write(cmd.encode('ascii'))
            except Exception as exc:
                self.get_logger().error(f'Serial write error: {exc}')


def main(args=None):
    parser = argparse.ArgumentParser(description='Devotics Arm V1 ESP32 Hardware Bridge')
    parser.add_argument(
        '--port',
        type=str,
        default=None,
        help='Serial port (e.g. /dev/ttyUSB0, /dev/ttyACM0, or socket://192.168.1.50:8888)',
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Print servo angle packets without opening serial port',
    )
    parsed_args, ros_args = parser.parse_known_args()

    rclpy.init(args=ros_args)
    node = DevoticsV1ESP32Bridge(port_override=parsed_args.port, dry_run=parsed_args.dry_run)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
