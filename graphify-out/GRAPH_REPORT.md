# Graph Report - devotics_arm_v1  (2026-11-15)

## Corpus Check
- 18 files · ~4,559 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 114 file(s) not represented in the graph (top: .stl 102, .xacro 3, (none) 2)

## Summary
- 94 nodes · 110 edges · 10 communities (7 shown, 3 thin omitted)
- Extraction: 80% EXTRACTED · 20% INFERRED · 0% AMBIGUOUS · INFERRED: 22 edges (avg confidence: 1.0)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3a871b71`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- PCA9685 PWM Driver
- moveit_configs_utils
- pick_and_place.py
- view_robot.launch.py
- esp32_bridge.py
- Devotics Arm V1 — Engineering Agent Directives
- moveit_launch.sh
- rules/graphify.md
- workflows/graphify.md
- DevoticsV1ESP32Bridge

## God Nodes (most connected - your core abstractions)
1. `DevoticsV1ESP32Bridge` - 9 edges
2. `DevoticsV1PickAndPlace` - 8 edges
3. `PCA9685 PWM Driver` - 8 edges
4. `Devotics Arm V1 — Engineering Agent Directives` - 5 edges
5. `J1 Base Yaw` - 4 edges
6. `J3 Elbow Pitch` - 4 edges
7. `J2 Shoulder Pitch` - 4 edges
8. `J4 Wrist Pitch` - 4 edges
9. `Gripper Actuator` - 3 edges
10. `ESP32 Controller` - 3 edges

## Surprising Connections (you probably didn't know these)
- `Devotics Arm V1` --GOVERNED_BY--> `Engineering Roadmap`  [INFERRED]
  README.md → docs/engineering_roadmap.md
- `Devotics Arm V1` --CONTAINS_JOINT--> `J1 Base Yaw`  [INFERRED]
  README.md → docs/mechanical_dimensions.md
- `Forearm STLs` --PHYSICAL_STRUCTURE_FOR--> `J3 Elbow Pitch`  [INFERRED]
  hardware/stl/Ante_Brazo_01.stl → docs/mechanical_dimensions.md
- `Base Assembly STLs` --PHYSICAL_STRUCTURE_FOR--> `J1 Base Yaw`  [INFERRED]
  hardware/stl/Base_01.stl → docs/mechanical_dimensions.md
- `Upper Arm STLs` --PHYSICAL_STRUCTURE_FOR--> `J2 Shoulder Pitch`  [INFERRED]
  hardware/stl/Brazo_01.stl → docs/mechanical_dimensions.md

## Import Cycles
- None detected.

## Communities (10 total, 3 thin omitted)

### Community 0 - "PCA9685 PWM Driver"
Cohesion: 0.16
Nodes (17): Base Assembly STLs, Devotics Arm V1, ESP32 Controller, Forearm STLs, Gripper Actuator, Gripper STLs, J1 Base Yaw, J2 Shoulder Pitch (+9 more)

### Community 2 - "pick_and_place.py"
Cohesion: 0.15
Nodes (11): builtin_interfaces_msg, control_msgs_action, DevoticsV1PickAndPlace, main(), Node, Devotics Arm V1 — Autonomous Pick & Place Mission Node Executes a complete…, Publishes the 3D target cube in RViz (either on the table or attached to tool0)., rclpy_action (+3 more)

### Community 3 - "view_robot.launch.py"
Cohesion: 0.20
Nodes (8): launch, launch_actions, launch_conditions, launch_ros_actions, launch_ros_parameter_descriptions, launch_ros_substitutions, launch_substitutions, os

### Community 4 - "esp32_bridge.py"
Cohesion: 0.20
Nodes (9): ament_index_python_packages, argparse, Devotics Arm V1 — Real-Time MoveIt 2 to ESP32 Physical Hardware Bridge…, math, rclpy, rclpy_node, sensor_msgs_msg, serial (+1 more)

### Community 5 - "Devotics Arm V1 — Engineering Agent Directives"
Cohesion: 0.33
Nodes (5): 1. Project Identity & Purpose, 2. Core Operational Rules for AI Agents, 3. Kinematic Architecture, 4. Current Stage & Next Steps, Devotics Arm V1 — Engineering Agent Directives

### Community 6 - "moveit_launch.sh"
Cohesion: 0.33
Nodes (4): ext_setup_bash, install_setup, moveit_launch.sh script, view_robot_launch.sh script

### Community 9 - "DevoticsV1ESP32Bridge"
Cohesion: 0.27
Nodes (4): DevoticsV1ESP32Bridge, main(), Node, JointState

## Knowledge Gaps
- **15 isolated node(s):** `moveit_launch.sh script`, `view_robot_launch.sh script`, `graphify`, `Workflow: graphify`, `1. Project Identity & Purpose` (+10 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 50 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DevoticsV1ESP32Bridge` connect `DevoticsV1ESP32Bridge` to `esp32_bridge.py`?**
  _High betweenness centrality (0.077) - this node is a cross-community bridge._
- **Are the 8 inferred relationships involving `PCA9685 PWM Driver` (e.g. with `ESP32 Controller` and `Gripper Actuator`) actually correct?**
  _`PCA9685 PWM Driver` has 8 INFERRED edges - model-reasoned connections that need verification._
- **What connects `moveit_launch.sh script`, `view_robot_launch.sh script`, `graphify` to the rest of the system?**
  _15 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `pick_and_place.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14705882352941177 - nodes in this community are weakly interconnected._