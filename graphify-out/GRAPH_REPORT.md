# Graph Report - devotics_arm_v1  (2026-10-02)

## Corpus Check
- Corpus is ~2,241 words - fits in a single context window. You may not need a graph.

## Summary
- 17 nodes · 22 edges · 4 communities
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 1,200 input · 800 output

## Community Hubs (Navigation)
- Community 0
- Community 1
- Community 2
- Community 3

## God Nodes (most connected - your core abstractions)
1. `PCA9685 PWM Driver` - 8 edges
2. `J1 Base Yaw` - 4 edges
3. `J2 Shoulder Pitch` - 4 edges
4. `J3 Elbow Pitch` - 4 edges
5. `J4 Wrist Pitch` - 4 edges
6. `J5 Wrist Roll` - 3 edges
7. `Gripper Actuator` - 3 edges
8. `ESP32 Controller` - 3 edges
9. `Devotics Arm V1` - 2 edges
10. `12V 20A SMPS & 6V Buck` - 2 edges

## Surprising Connections (you probably didn't know these)
- `Devotics Arm V1` --CONTAINS_JOINT--> `J1 Base Yaw`  [EXTRACTED]
  README.md → docs/mechanical_dimensions.md
- `Devotics Arm V1` --GOVERNED_BY--> `Engineering Roadmap`  [EXTRACTED]
  README.md → docs/engineering_roadmap.md
- `Base Assembly STLs` --PHYSICAL_STRUCTURE_FOR--> `J1 Base Yaw`  [EXTRACTED]
  hardware/stl/Base_01.stl → docs/mechanical_dimensions.md
- `Upper Arm STLs` --PHYSICAL_STRUCTURE_FOR--> `J2 Shoulder Pitch`  [EXTRACTED]
  hardware/stl/Brazo_01.stl → docs/mechanical_dimensions.md
- `Forearm STLs` --PHYSICAL_STRUCTURE_FOR--> `J3 Elbow Pitch`  [EXTRACTED]
  hardware/stl/Ante_Brazo_01.stl → docs/mechanical_dimensions.md

## Communities (4 total, 0 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.40
Nodes (5): Gripper Actuator, Gripper STLs, J4 Wrist Pitch, J5 Wrist Roll, Wrist STLs

### Community 1 - "Community 1"
Cohesion: 0.50
Nodes (4): Base Assembly STLs, Devotics Arm V1, J1 Base Yaw, Engineering Roadmap

### Community 2 - "Community 2"
Cohesion: 0.67
Nodes (4): ESP32 Controller, PCA9685 PWM Driver, 12V 20A SMPS & 6V Buck, ROS 2 Jazzy Workstation

### Community 3 - "Community 3"
Cohesion: 0.50
Nodes (4): Forearm STLs, J2 Shoulder Pitch, J3 Elbow Pitch, Upper Arm STLs

## Knowledge Gaps
- **7 isolated node(s):** `ROS 2 Jazzy Workstation`, `Engineering Roadmap`, `Base Assembly STLs`, `Upper Arm STLs`, `Forearm STLs` (+2 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 7 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PCA9685 PWM Driver` connect `Community 2` to `Community 0`, `Community 1`, `Community 3`?**
  _High betweenness centrality (0.650) - this node is a cross-community bridge._
- **Why does `J1 Base Yaw` connect `Community 1` to `Community 2`, `Community 3`?**
  _High betweenness centrality (0.342) - this node is a cross-community bridge._
- **Why does `J2 Shoulder Pitch` connect `Community 3` to `Community 1`, `Community 2`?**
  _High betweenness centrality (0.158) - this node is a cross-community bridge._
- **What connects `ROS 2 Jazzy Workstation`, `Engineering Roadmap`, `Base Assembly STLs` to the rest of the system?**
  _7 weakly-connected nodes found - possible documentation gaps or missing edges._