# Devotics Arm V1 — Mechanical Dimensions & Reverse Engineering

> **Engineering Rule 1:** Never guess dimensions when they can be measured.  
> The ROS link dimensions must represent **joint-axis center → next joint-axis center**, not the outer physical bounding box of 3D prints.

## 1. Kinematic Link Length Table

| Joint / Segment | Measured Distance (mm) | Rotation Axis `[x, y, z]` | Primary STL Files | Confidence | Status / Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Base → J1 (Base Yaw)** | *TBD* | `[0, 0, 1]` | `Base_01.stl`, `Base_02.stl`, `Base_03.stl` | UNVERIFIED | Distance from table mount to base rotation axis |
| **J1 → J2 (Shoulder Pitch)** | *TBD* | `[0, 1, 0]` | `Base_04.stl`, `Brazo_01.stl` | UNVERIFIED | Vertical Z-offset from J1 center to J2 shoulder axis |
| **J2 → J3 (Elbow Pitch)** | *TBD* (~245mm part) | `[0, 1, 0]` | `Brazo_01.stl`, `Brazo_02.stl`, `Brazo_03.stl` | UNVERIFIED | True center-to-center distance of upper arm |
| **J3 → J4 (Wrist Pitch)** | *TBD* (~188mm part) | `[0, 1, 0]` | `Ante_Brazo_01.stl`, `Control_AnteBrazo02.stl` | UNVERIFIED | True center-to-center distance of forearm |
| **J4 → J5 (Wrist Roll)** | *TBD* (~115mm part) | `[1, 0, 0]` | `Munequilla_01.stl` | UNVERIFIED | Offset from pitch hinge to axial roll axis |
| **J5 → TCP (Tool Center Point)**| *TBD* | N/A (Fixed TCP) | `Brida_Pinza_01.stl`, `Pinza_01`..`05` | UNVERIFIED | Center point between grasping finger pads |

---

## 2. Component Inventory & STL Mapping

| Category | Component File(s) | Function / Subsystem | Connected Link |
| :--- | :--- | :--- | :--- |
| **Base Assembly** | `Base_01.stl`<br>`Base_02.stl`<br>`Base_03.stl`<br>`Base_04.stl` | Table mounting plate, main bearing housing, J1 servo mount, rotating turret | `base_link`<br>`base_rotation_link` |
| **Upper Arm** | `Brazo_01.stl`<br>`Brazo_02.stl`<br>`Brazo_03.stl` | Main shoulder arm structure, spring anchors, J3 servo pocket | `upper_arm_link` |
| **Forearm** | `Ante_Brazo_01.stl`<br>`Control_AnteBrazo02.stl` | Forearm linkage, push-rod guide / parallel bar | `forearm_link` |
| **Wrist** | `Munequilla_01.stl`<br>`Tapa_servo.stl` | Pitch/Roll gimbal assembly, servo mounts | `wrist_pitch_link`<br>`wrist_roll_link` |
| **Gripper / End-Effector**| `Pinza_01.stl` ... `Pinza_05.stl`<br>`Brida_Pinza_01.stl`<br>`Engranaje_01.stl`, `02.stl` | Finger linkages, flange adapter, spur drive gears | `gripper_base_link`<br>`gripper_finger_links` |
| **Hardware & Rigging** | `Pin_Muelle.stl`<br>`soporte_muelle.stl`<br>`Jaula_bolas.stl`<br>`Tapa_rodamiento.stl`<br>`Grapa_cables_01`..`05.stl` | Spring retainer pins, spring mounts, ball bearing cage, cable routing clips | Non-kinematic structural attachments |

---

## 3. Action Items for Verification
1. Place raw STL files into `hardware/stl/`.
2. Inspect pivot holes and bearing recesses in CAD or mesh inspection tool.
3. Measure center-of-hole to center-of-hole for each segment.
4. Record verified values and change Confidence status from `UNVERIFIED` to `VERIFIED`.
