# Graph Report - devotics_arm_v1  (2026-11-15)

## Corpus Check
- 17 files · ~3,859 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 113 file(s) not represented in the graph (top: .stl 102, .xacro 3, (none) 2)

## Summary
- 77 nodes · 85 edges · 9 communities (6 shown, 3 thin omitted)
- Extraction: 74% EXTRACTED · 26% INFERRED · 0% AMBIGUOUS · INFERRED: 22 edges (avg confidence: 1.0)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `29f9afbf`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- PCA9685 PWM Driver
- moveit_configs_utils
- pick_and_place.py
- view_robot.launch.py
- DevoticsV1PickAndPlace
- Devotics Arm V1 — Engineering Agent Directives
- moveit_launch.sh
- rules/graphify.md
- workflows/graphify.md

## God Nodes (most connected - your core abstractions)
1. `DevoticsV1PickAndPlace` - 8 edges
2. `PCA9685 PWM Driver` - 8 edges
3. `Devotics Arm V1 — Engineering Agent Directives` - 5 edges
4. `J4 Wrist Pitch` - 4 edges
5. `J1 Base Yaw` - 4 edges
6. `J3 Elbow Pitch` - 4 edges
7. `J2 Shoulder Pitch` - 4 edges
8. `Gripper Actuator` - 3 edges
9. `J5 Wrist Roll` - 3 edges
10. `ESP32 Controller` - 3 edges

## Surprising Connections (you probably didn't know these)
- `Wrist STLs` --PHYSICAL_STRUCTURE_FOR--> `J4 Wrist Pitch`  [INFERRED]
  hardware/stl/Munequilla_01.stl → docs/mechanical_dimensions.md
- `Gripper STLs` --PHYSICAL_STRUCTURE_FOR--> `Gripper Actuator`  [INFERRED]
  hardware/stl/Pinza_01.stl → docs/mechanical_dimensions.md
- `Devotics Arm V1` --GOVERNED_BY--> `Engineering Roadmap`  [INFERRED]
  README.md → docs/engineering_roadmap.md
- `Devotics Arm V1` --CONTAINS_JOINT--> `J1 Base Yaw`  [INFERRED]
  README.md → docs/mechanical_dimensions.md
- `Base Assembly STLs` --PHYSICAL_STRUCTURE_FOR--> `J1 Base Yaw`  [INFERRED]
  hardware/stl/Base_01.stl → docs/mechanical_dimensions.md

## Import Cycles
- None detected.

## Communities (9 total, 3 thin omitted)

### Community 0 - "PCA9685 PWM Driver"
Cohesion: 0.16
Nodes (17): Base Assembly STLs, Devotics Arm V1, ESP32 Controller, Forearm STLs, Gripper Actuator, Gripper STLs, J1 Base Yaw, J2 Shoulder Pitch (+9 more)

### Community 2 - "pick_and_place.py"
Cohesion: 0.17
Nodes (11): argparse, builtin_interfaces_msg, control_msgs_action, main(), Devotics Arm V1 — Autonomous Pick & Place Mission Node Executes a complete…, rclpy, rclpy_action, rclpy_node (+3 more)

### Community 3 - "view_robot.launch.py"
Cohesion: 0.20
Nodes (8): launch, launch_actions, launch_conditions, launch_ros_actions, launch_ros_parameter_descriptions, launch_ros_substitutions, launch_substitutions, os

### Community 4 - "DevoticsV1PickAndPlace"
Cohesion: 0.36
Nodes (3): DevoticsV1PickAndPlace, Publishes the 3D target cube in RViz (either on the table or attached to tool0)., Node

### Community 5 - "Devotics Arm V1 — Engineering Agent Directives"
Cohesion: 0.33
Nodes (5): 1. Project Identity & Purpose, 2. Core Operational Rules for AI Agents, 3. Kinematic Architecture, 4. Current Stage & Next Steps, Devotics Arm V1 — Engineering Agent Directives

### Community 6 - "moveit_launch.sh"
Cohesion: 0.33
Nodes (4): ext_setup_bash, install_setup, moveit_launch.sh script, view_robot_launch.sh script

## Knowledge Gaps
- **15 isolated node(s):** `moveit_launch.sh script`, `view_robot_launch.sh script`, `graphify`, `Workflow: graphify`, `1. Project Identity & Purpose` (+10 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 46 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DevoticsV1PickAndPlace` connect `DevoticsV1PickAndPlace` to `pick_and_place.py`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Are the 8 inferred relationships involving `PCA9685 PWM Driver` (e.g. with `ESP32 Controller` and `Gripper Actuator`) actually correct?**
  _`PCA9685 PWM Driver` has 8 INFERRED edges - model-reasoned connections that need verification._
- **What connects `moveit_launch.sh script`, `view_robot_launch.sh script`, `graphify` to the rest of the system?**
  _15 weakly-connected nodes found - possible documentation gaps or missing edges._