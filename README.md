# Devotics Arm V1

**Devotics Arm V1** is a 5-DOF articulated desktop/benchtop research robotic arm with a gripper end-effector, built for robotics research, ROS 2 learning, kinematics, motion planning (MoveIt 2), ros2_control, teleoperation, and autonomous pick-and-place experiments.

> **Engineering Philosophy:**  
> `inspect → measure → model → simulate → validate → control → integrate hardware → test`  
> Keep V1 measurable, understandable, reproducible, and maintainable.

---

## 1. Robot Configuration Overview

- **Arm Type:** 5-DOF Articulated Manipulator + Actuated Gripper
- **Target Reach:** ~500+ mm (to be extracted from mechanical geometry)
- **Target Scale:** ~600 mm overall physical envelope
- **Primary Actuators:** 5 × MG996R (J1-J5) + MG90S (Gripper)
- **Controller Stack:** ROS 2 Jazzy (Ubuntu 24.04) → ESP32 → PCA9685 (16-channel PWM driver)
- **Power Delivery:** 12V 20A SMPS → High-Current Buck Converter (~6V Rail)

### Kinematic Chain Concept
```text
world
  └── base_link
        └── J1 (Yaw / Base rotation)
              └── base_rotation_link
                    └── J2 (Shoulder pitch)
                          └── upper_arm_link
                                └── J3 (Elbow pitch)
                                      └── forearm_link
                                            └── J4 (Wrist pitch)
                                                  └── wrist_pitch_link
                                                        └── J5 (Wrist roll)
                                                              └── wrist_roll_link
                                                                    └── gripper_base_link
                                                                          └── tool0 / TCP
```

---

## 2. Repository Layout

```text
devotics_arm_v1_ws/
└── src/
    └── devotics_arm_v1/
        ├── devotics_arm_description/    # URDF/Xacro, meshes, RViz configs, materials
        ├── devotics_arm_moveit_config/  # MoveIt 2 SRDF, kinematics, controllers
        ├── devotics_arm_control/        # ros2_control hardware interfaces / bridges
        ├── devotics_arm_bringup/        # High-level launch files & orchestration
        ├── firmware/                    # ESP32 firmware modules (calibration, teleop, bridge)
        ├── hardware/                    # CAD, STL models, wiring diagrams, measurements
        ├── docs/                        # Engineering documentation & build logs
        └── README.md
```

---

## 3. Capability Roadmap

- [ ] **V1.0 — Mechanical Prototype:** Component identification, measurement, structural assembly.
- [ ] **V1.1 — Joint Validation:** Independent J1–J5 safe limit determination & home calibration.
- [ ] **V1.2 — Full Manual Motion:** ESP32 + PCA9685 smooth coordinated motion.
- [ ] **V1.3 — Manual Teleoperation:** Potentiometer control with calibrated mapping.
- [ ] **V1.4 — Gripper:** Reliable grasping and object handling.
- [ ] **V1.5 — Teach & Repeat:** Waypoint recording & smooth trajectory playback.
- [ ] **V1.6 — Digital Twin:** Primitive URDF → Verified kinematic mesh model in RViz.
- [ ] **V1.7 — ROS Hardware Integration:** ros2_control serial bridge to ESP32.
- [ ] **V1.8 — MoveIt 2:** Motion planning, collision matrices, IK validation.
- [ ] **V1.9 — Autonomous Manipulation:** Repeatable autonomous pick-and-place demonstration.
