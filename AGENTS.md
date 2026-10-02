# Devotics Arm V1 — Engineering Agent Directives

## 1. Project Identity & Purpose
You are working on **Devotics Arm V1**, a 5-DOF articulated desktop research robotic arm with an actuated gripper.
- **Classification:** Educational & Research Manipulator (NOT industrial-grade).
- **Primary Mission:** Kinematics, ROS 2 Jazzy control, MoveIt 2 motion planning, teleoperation, and autonomous pick-and-place experiments.
- **Hardware Profile:**
  - J1 (Base Yaw): MG996R
  - J2 (Shoulder Pitch): MG996R (Dual-spring gravity assist)
  - J3 (Elbow Pitch): MG996R
  - J4 (Wrist Pitch): MG996R
  - J5 (Wrist Roll): MG996R
  - Gripper: MG90S
  - Electronics: ESP32 + PCA9685 (16-channel PWM driver)
  - Power: 12V 20A SMPS -> ~6V High-Current Buck Converter -> Common Ground

---

## 2. Core Operational Rules for AI Agents

1. **Step-by-Step Guidance:** Do NOT rush ahead and generate massive amounts of unvalidated code. Guide the user interactively through each milestone.
2. **Never Guess Dimensions:** Every kinematic link length must be measured from **joint-axis center to next joint-axis center** from the CAD / STL models or physical calipers. Never use bounding-box lengths.
3. **Engineering Sequence:** Strictly adhere to:
   $$\text{inspect} \longrightarrow \text{measure} \longrightarrow \text{model} \longrightarrow \text{simulate} \longrightarrow \text{validate} \longrightarrow \text{control} \longrightarrow \text{integrate} \longrightarrow \text{test}$$
4. **Isolate Subsystems:** Do not debug ROS control and physical electronics simultaneously. Verify mechanical pivots -> then primitive URDF -> then servo calibration -> then ROS control.
5. **No Industrial Claims:** Do not claim high payload or precision without empirical measurement. V1 payload target is ~20g-50g nominal.
6. **Preserve V0 Independence:** V0 in `ros2_ws` is a separate baseline. Do not overwrite or contaminate V0.
7. **Commit Often:** Commit git milestones cleanly.

---

## 3. Kinematic Architecture

```text
world
  └── base_link
        └── J1 (Yaw / Base rotation) [Axis: 0, 0, 1]
              └── base_rotation_link
                    └── J2 (Shoulder pitch) [Axis: 0, 1, 0]
                          └── upper_arm_link
                                └── J3 (Elbow pitch) [Axis: 0, 1, 0]
                                      └── forearm_link
                                            └── J4 (Wrist pitch) [Axis: 0, 1, 0]
                                                  └── wrist_pitch_link
                                                        └── J5 (Wrist roll) [Axis: 1, 0, 0]
                                                              └── wrist_roll_link
                                                                    └── gripper_base_link
                                                                          └── tool0 / TCP
```

---

## 4. Current Stage & Next Steps
- **Active Stage:** **Stage 1 — Mechanical Reverse Engineering & Joint Center Extraction**
- **Action Required:** Inspect STL files in `hardware/stl/` (or CAD) to extract real center-to-center distances and populate `docs/mechanical_dimensions.md`.
- **Roadmap Reference:** See `docs/engineering_roadmap.md` for full breakdown of all 10 stages (V1.0 through V1.9).
