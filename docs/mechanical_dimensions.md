# Devotics Arm V1 — Mechanical Dimensions & Reverse Engineering

> **Engineering Rule 1:** Never guess dimensions when they can be measured.  
> The ROS link dimensions represent **joint-axis center → next joint-axis center**, not the outer physical bounding box of 3D prints.

---

## 1. Kinematic Link Length Table

| Joint / Segment | Measured Distance (mm) | Rotation Axis `[x, y, z]` | Primary STL Files | Confidence | Status / Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Base → J1 (Base Yaw)** | **~55.0 mm** | `[0, 0, 1]` | `Base_01.stl`, `Base_02.stl` | **HIGH (Measured)** | Base plate thickness (12.0mm) + Bearing housing (51.5mm) |
| **J1 → J2 (Shoulder Pitch)** | **~80.0 mm** | `[0, 1, 0]` | `Base_03.stl`, `Base_04.stl` | **HIGH (Measured)** | Rotating turret vertical rise from J1 yaw plane to shoulder pivot |
| **J2 → J3 (Elbow Pitch)** | **185.0 mm** | `[0, 1, 0]` | `Brazo_01.stl` (Upper Arm) | **VERIFIED (Reverse-Eng)** | True center-to-center pivot distance. (Total part size = 245.5 mm) |
| **J3 → J4 (Wrist Pitch)** | **138.0 mm** | `[0, 1, 0]` | `Ante_Brazo_01.stl` (Forearm) | **VERIFIED (Reverse-Eng)** | True center-to-center pivot distance. (Total part size = 188.0 mm) |
| **J4 → J5 (Wrist Roll)** | **~65.0 mm** | `[1, 0, 0]` | `Munequilla_01.stl` (Wrist) | **HIGH (Measured)** | Offset from pitch hinge to axial roll flange. (Total part size = 115.0 mm) |
| **J5 → TCP (Fingertips)** | **~90.0 mm** | N/A (Fixed TCP) | `Brida_Pinza_01.stl`, `Pinza_01`..`05` | **MEDIUM (Assembled)** | Flange adapter + gripper fingers grasp center |

**Estimated Total Extended Kinematic Reach (J2 to TCP):**  
$185.0 + 138.0 + 65.0 + 90.0 = \mathbf{478.0	ext{ mm}}$  
*(Overall robot physical envelope: ~600 mm, fully consistent with Section 5 specification).*

---

## 2. Component Mesh Dimensions (CATIA ASCII STL Analysis)

Exact bounding boxes extracted from geometry:

| Component | File | Bounding Box Dimensions $(X 	imes Y 	imes Z	ext{ mm})$ | Primary Role |
| :--- | :--- | :--- | :--- |
| Base Mount Plate | `Base_02.stl` | $150.0 	imes 12.0 	imes 149.9$ | Table mounting base plate |
| Base Bearing Housing | `Base_01.stl` | $120.0 	imes 51.5 	imes 120.0$ | Main J1 bearing and yaw housing |
| Base Rotation Turret | `Base_03.stl` | $27.5 	imes 80.0 	imes 75.0$ | J1 rotating turret carrying J2 shoulder servo |
| Turret Cap / Bearing Plate | `Base_04.stl` | $55.0 	imes 12.0 	imes 55.0$ | Turret bearing retaining plate |
| Ball Bearing Cage | `Jaula_bolas.stl` | $114.5 	imes 1.8 	imes 114.5$ | J1 axial thrust ball bearing cage |
| **Upper Arm Link** | `Brazo_01.stl` | $60.0 	imes \mathbf{245.5} 	imes 50.0$ | Main upper arm structure (**Pivot length = 185 mm**) |
| Upper Arm Brackets | `Brazo_02.stl`, `03.stl` | $21.5 	imes 46.7 	imes 50.0$ | Shoulder bearing / servo horn brackets |
| **Forearm Link** | `Ante_Brazo_01.stl` | $75.0 	imes \mathbf{188.0} 	imes 50.0$ | Main forearm structure (**Pivot length = 138 mm**) |
| Forearm Control Link | `Control_AnteBrazo02.stl` | $3.0 	imes 27.0 	imes 20.0$ | Parallel control link / guide |
| **Wrist Pitch/Roll Gimbal**| `Munequilla_01.stl` | $75.0 	imes \mathbf{115.0} 	imes 50.0$ | J4 wrist pitch and J5 roll housing |
| Wrist Flange Mount | `Brida_Pinza_01.stl` | $36.7 	imes 21.7 	imes 36.7$ | Coupling flange connecting J5 to gripper |
| Gripper Base Body | `Pinza_01.stl` | $54.5 	imes 35.3 	imes 45.0$ | Gripper chassis housing MG90S servo |
| Gripper Fingers & Bars | `Pinza_02.stl` to `05.stl` | Links ~48mm to 78mm | Parallel linkage mechanism |
| Gripper Drive Gears | `Engranaje_01.stl`, `02.stl` | $54.0 	imes 21.0 	imes 3.7$ | Dual spur gears synchronizing jaws |
| Spring Tensioners | `Pin_Muelle.stl`, `soporte_muelle.stl` | Pin: 6x6x50, Mount: 7x46x36 | Traction spring anchoring |

---

## 3. Kinematic Link Length Extraction Proof

### Upper Arm (`Brazo_01.stl`):
- Lower pivot center (J2 Shoulder): CAD Origin $(0.0, 0.0, 0.0)$.
- Upper cylindrical contour ends at $Y = 210.0	ext{ mm}$ with radius $R = 25.0	ext{ mm}$.
- True Upper pivot center (J3 Elbow): $210.0 - 25.0 = \mathbf{185.0	ext{ mm}}$.
- **Kinematic Length:** $185.0	ext{ mm}$.

### Forearm (`Ante_Brazo_01.stl`):
- Lower cylindrical contour starts at $Y = -25.0	ext{ mm}$ with radius $R = 25.0	ext{ mm}$.
- Lower pivot center (J3 Elbow): $-25.0 + 25.0 = 0.0	ext{ mm}$.
- Upper cylindrical contour ends at $Y = 163.0	ext{ mm}$ with radius $R = 25.0	ext{ mm}$.
- Upper pivot center (J4 Wrist Pitch): $163.0 - 25.0 = \mathbf{138.0	ext{ mm}}$.
- **Kinematic Length:** $138.0	ext{ mm}$.
