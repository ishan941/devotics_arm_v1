# Devotics Arm V1 — Comprehensive Engineering Roadmap

## Overview & Methodology
This roadmap breaks the development of Devotics Arm V1 into sequential, milestone-gated stages. Each stage must satisfy its completion criteria before moving to the next.

```text
Stage 1: Mechanical Inspection & Dimension Extraction (CURRENT)
   ↓
Stage 2: Primitive Xacro / URDF & TF2 Validation in RViz
   ↓
Stage 3: High-Fidelity Visual & Collision Mesh Integration
   ↓
Stage 4: Actuator Bench Testing & Calibration (ESP32 + PCA9685)
   ↓
Stage 5: Manual Teleoperation (Potentiometers / Web / Serial)
   ↓
Stage 6: Teach-and-Repeat Trajectory Engine
   ↓
Stage 7: ros2_control Hardware Interface (Mock -> Serial Bridge)
   ↓
Stage 8: MoveIt 2 Motion Planning & Collision Matrix
   ↓
Stage 9: Cartesian Kinematics & Palletizing / Pick-and-Place
   ↓
Stage 10: System Hardening, Repeatability Validation & Documentation
```

---

## Detailed Stages

### Stage 1: Mechanical Reverse Engineering (V1.0 Prep)
- **Goal:** Extract real kinematic pivot distances and joint axes from the 3D STL files in `hardware/stl/`.
- **Key Files:**
  - `Base_01.stl` to `Base_04.stl`: Base mount, yaw bearing, shoulder pivot.
  - `Brazo_01.stl` to `Brazo_03.stl`: Upper arm link (~245 mm physical).
  - `Ante_Brazo_01.stl`, `Control_AnteBrazo02.stl`: Forearm link (~188 mm physical).
  - `Munequilla_01.stl`: Wrist pitch/roll gimbal (~115 mm physical).
  - `Pinza_01.stl` to `05.stl`, `Brida_Pinza_01.stl`, `Engranaje_01`/`02.stl`: Gripper assembly.
- **Deliverable:** Fully populated `docs/mechanical_dimensions.md` with zero guesswork.

### Stage 2: Digital Twin Foundation — Primitives Only
- **Goal:** Build `devotics_arm_description` using simple geometric primitives (cylinders, boxes).
- **Validation:**
  - Confirm coordinate frames: X=Forward, Y=Left, Z=Up.
  - Verify joint rotation directions with right-hand rule.
  - Validate TF tree continuity with `tf2_tools view_frames`.
  - RViz visualization with `joint_state_publisher_gui`.

### Stage 3: Visual & Simplified Collision Mesh Integration
- **Goal:** Connect clean visual STLs and lightweight collision primitives.
- **Validation:**
  - Check mesh origins and scaling (convert mm to meters if needed).
  - Fast collision checking without polygon overload.

### Stage 4: Electronics & Joint Calibration (Firmware V1.1)
- **Goal:** ESP32 + PCA9685 bench setup.
- **Tasks:**
  - Verify 6V power rail stability under no-load and stall conditions.
  - Determine physical mechanical stops vs safe software servo limits.
  - Create centralized calibration table (angle -> PWM microsecond mapping).

### Stage 5: Manual Teleoperation (Firmware V1.3)
- **Goal:** Direct analog control via potentiometers.
- **Features:** ADC reading, software low-pass filtering, smooth velocity ramping, joint limit enforcement.

### Stage 6: Standalone Teach-and-Repeat Engine (Firmware V1.5)
- **Goal:** Offline pose recording and trajectory interpolation without ROS connection.
- **Validation:** Smooth multi-waypoint playback without violent servo jerking.

### Stage 7: ROS 2 Control Integration (V1.7)
- **Goal:** Implement `ros2_control` hardware abstraction.
- **Phases:**
  1. `mock_components/GenericSystem`
  2. `JointTrajectoryController` configuration
  3. Custom USB Serial bridge between ROS 2 node and ESP32.

### Stage 8: MoveIt 2 Pipeline (V1.8)
- **Goal:** Automated trajectory generation and obstacle avoidance.
- **Tasks:**
  - Generate `devotics_arm_moveit_config`.
  - Define planning groups (`arm`: J1-J5, `gripper`).
  - Generate Self-Collision Matrix (ACM).
  - Configure KDL / PickIK / OMPL solver.

### Stage 9: Manipulation & Autonomous Pick-and-Place (V1.9)
- **Goal:** End-to-end autonomous object manipulation.
- **Tasks:**
  - Cartesian linear motion planning.
  - Palletizing demonstration (e.g. pick from grid, place to stack).

### Stage 10: Validation Metrics & Engineering Signoff
- **Goal:** Empirical characterization.
- **Metrics:** TCP repeatability (20 cycles), maximum payload at full extension vs retracted, thermal monitoring of J2 shoulder, voltage drop log.
