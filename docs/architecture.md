# Devotics Arm V1 — System Architecture

## 1. System Overview
Devotics Arm V1 decouples mechanical modeling, embedded actuation, and high-level ROS 2 computation to allow strict verification of each layer.

```text
+-------------------------------------------------------------+
|                     ROS 2 Workstation                       |
|  - MoveIt 2 Motion Planner (OMPL / Pilz)                   |
|  - JointTrajectoryController / ros2_control                 |
|  - Robot State Publisher & TF2                              |
|  - Teleop & Autonomous Nodes                                |
+------------------------------+------------------------------+
                               | USB Serial (115200 / 921600 baud)
                               v
+-------------------------------------------------------------+
|                     ESP32 Microcontroller                   |
|  - Command parsing & safety watchdog                        |
|  - Multi-joint trajectory interpolation (smooth ramping)    |
|  - Joint angle to servo PWM microsecond mapping             |
|  - Hardware emergency stop / limit protection               |
+------------------------------+------------------------------+
                               | I2C Interface (Fast-mode 400kHz)
                               v
+-------------------------------------------------------------+
|                  PCA9685 16-Channel PWM Driver              |
|  - Hardware 50Hz PWM output                                 |
+------------------------------+------------------------------+
                               | Individual PWM Signal Lines
                               v
+-------------------------------------------------------------+
|                        Actuators                            |
|  - J1 (Base Yaw):      MG996R                               |
|  - J2 (Shoulder):      MG996R (Dual-spring gravity assist)  |
|  - J3 (Elbow):         MG996R                               |
|  - J4 (Wrist Pitch):   MG996R                               |
|  - J5 (Wrist Roll):    MG996R                               |
|  - Gripper:            MG90S                                |
+-------------------------------------------------------------+
```

## 2. Power System Architecture
High-current servos under load (especially J2 shoulder) demand significant instantaneous currents (>2.5A peak per servo). Power delivery must prevent ESP32 brownouts and voltage sag.

```text
230V AC Mains
     │
     ▼
[ 12V 20A SMPS ]
     ├─────────────────────────────────────────┐
     ▼                                         ▼
[ LM2596 / 5V Reg ]                      [ 300W 20A Buck Converter ]
     │                                         │ (Adjusted to ~6.0V DC)
     ▼                                         ▼
 ESP32 (Vin / 5V)                        [ 4700µF Low-ESR Cap ]
                                               │
                                               ├────────► PCA9685 V+ Rail
                                               └────────► Servos Power Rail
[ COMMON GROUND: ESP32 GND <=====> PCA9685 GND <=====> Power Rail GND ]
```

## 3. Coordinate Frames & Conventions
Follows standard ROS coordinate conventions:
- **X:** Forward
- **Y:** Left
- **Z:** Up
- Right-hand rule applies for all joint rotational axes.
