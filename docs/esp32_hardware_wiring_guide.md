# Devotics Arm V1 — Complete ESP32 + PCA9685 Hardware Wiring & Bringup Guide

This guide walks you step-by-step through wiring your **12V 20A SMPS**, **10A/100W Buck Converter**, **PCA9685 16-Channel PWM Driver**, **ESP32**, and **6 Servos (3× MG996R + 3× MG90S)**, calibrating the joints safely, and running **MoveIt 2 + Autonomous Pick-and-Place** on the physical robot arm.

---

## 1. Bill of Materials (Electronics & Actuators)

| Component | Quantity | Specification / Role |
| :--- | :---: | :--- |
| **Main Power Supply (SMPS)** | 1 | `12V DC, 20A` Switching Power Supply |
| **DC-DC Step-Down Buck Converter** | 1 | `10A / 100W (12A Max)` (`5–40V IN` → `1.2–36V OUT`) |
| **Servo PWM Driver** | 1 | **PCA9685** 16-Channel 12-bit I2C PWM Servo Driver |
| **Microcontroller** | 1 | **ESP32 DevKit V1** (30-pin or 38-pin, USB Serial) |
| **Heavy Load Joints (`J1, J2, J3`)** | 3 | **MG996R** Metal-Gear Servos (Base Yaw, Shoulder Pitch, Elbow Pitch) |
| **Wrist & Gripper Joints (`J4, J5, J6`)** | 3 | **MG90S** Micro Metal-Gear Servos (Wrist Pitch, Wrist Roll, Gripper) |

---

## 2. Step 1 — Set the Buck Converter Voltage FIRST (Critical Safety Step!)

> [!CAUTION]
> **DO NOT connect the PCA9685 or any servos to the Buck Converter until you have tuned the output voltage with a multimeter!**
> - **MG996R** operating range: `4.8V – 6.6V`
> - **MG90S** operating range: `4.8V – 6.0V MAX` (Voltages above `6.0V` will permanently burn out the small MG90S control boards under load).

### Voltage Tuning Procedure:
1. Leave the **OUT+** and **OUT-** terminals of the Buck Converter **disconnected**.
2. Connect the **12V 20A SMPS** to the Buck Converter input:
   - SMPS **`+V (+12V)`** $\longrightarrow$ Buck Converter **`IN+`**
   - SMPS **`-V (GND)`** $\longrightarrow$ Buck Converter **`IN-`**
3. Turn on the SMPS and place your **Multimeter** probes (set to DC Volts) across Buck Converter **`OUT+`** and **`OUT-`**.
4. Turn the small brass screw on the Buck Converter's blue potentiometer (usually counter-clockwise to lower voltage) until your multimeter reads:
   $$\mathbf{5.6\text{ V} \text{ to } 5.8\text{ V}} \quad (\text{Ideal target: } \mathbf{5.7\text{ V}})$$
5. Turn **OFF** the SMPS before wiring the PCA9685.

---

## 3. Step 2 — Complete Power & Logic Wiring Diagram

```text
================================================================================
                        POWER DISTRIBUTION (HIGH CURRENT)
================================================================================

 [ 220V AC Mains ]
        │
        ▼
 [ 12V 20A SMPS ]
   ├── (+V) +12V ──────► [ IN+ ]  10A/100W Buck Converter  [ OUT+ (+5.7V) ] ───┐
   └── (-V)  GND ──────► [ IN- ]  (Adjusted to 5.7V DC!)   [ OUT- (GND)   ] ─┐ │
                                                                             │ │
                                           ┌─────────────────────────────────┘ │
                                           ▼                                   ▼
                                   ┌───────────────┐                   ┌───────────────┐
                                   │      GND      │                   │      V+       │
                                   └───────┬───────┴───────────────────┴───────┬───────┘
                                           │   PCA9685 Green Screw Terminal    │
                                           └───────────────────────────────────┘


================================================================================
                        LOGIC & I2C WIRING (ESP32 ↔ PCA9685)
================================================================================

  ┌─────────────────────┐                         ┌─────────────────────────────────┐
  │    ESP32 DevKit     │                         │     PCA9685 Left Side Header    │
  │                     │                         │                                 │
  │         3V3 (3.3V)  ├────────────────────────►│ VCC  (3.3V Logic Power ONLY)    │
  │                GND  ├────────────────────────►│ GND  (Common Ground)            │
  │      GPIO 21 (SDA)  ├────────────────────────►│ SDA  (I2C Data)                 │
  │      GPIO 22 (SCL)  ├────────────────────────►│ SCL  (I2C Clock)                │
  │                     │                         │ OE   (Leave Unconnected)        │
  │          [USB Port] │                         │ V+   (Leave Side Pin Empty!)    │
  └──────────────┬──────┘                         └─────────────────────────────────┘
                 │
                 ▼
       [ Ubuntu PC USB Port ]
         (/dev/ttyUSB0)
```

### ESP32 ↔ PCA9685 Pin-by-Pin Table
| PCA9685 Left Header Pin | Connect to ESP32 Pin | Wire Role & Notes |
| :--- | :--- | :--- |
| **`VCC`** | **`3V3` (3.3V)** | Powers the PCA9685 logic chip at 3.3V (safe for ESP32 I2C pins) |
| **`GND`** | **`GND`** | **Crucial:** Establishes common ground between ESP32 and PCA9685 |
| **`SDA`** | **`GPIO 21`** | I2C Data line |
| **`SCL`** | **`GPIO 22`** | I2C Clock line |
| **`OE`** | *Not connected* | Pulled low on board by default (outputs enabled) |
| **`V+`** *(side header)* | *Not connected* | Servo power enters through the **top green screw terminal** instead |

---

## 4. Step 3 — Plugging the 6 Servos into PCA9685 (`CH0` to `CH5`)

Each servo has a 3-pin connector:
- **Yellow / Orange wire** = **`PWM` (Signal — Top row on PCA9685)**
- **Red wire** = **`V+` (+5.7V Power — Middle row on PCA9685)**
- **Brown / Black wire** = **`GND` (Ground — Bottom row on PCA9685)**

| PCA9685 Channel | Robot Joint Name | Physical Joint Role | Servo Model | Home Angle (`0 rad` in ROS) |
| :---: | :--- | :--- | :---: | :---: |
| **`CH0`** | `joint_1` (`J1`) | **Base Yaw** (Left/Right rotation) | **MG996R #1** | `90°` |
| **`CH1`** | `joint_2` (`J2`) | **Shoulder Pitch** (`Eje Central` → `Antebrazo`) | **MG996R #2** | `90°` |
| **`CH2`** | `joint_3` (`J3`) | **Elbow Pitch** (`Antebrazo` → `Brazo`) | **MG996R #3** | `90°` |
| **`CH3`** | `joint_4` (`J4`) | **Wrist Pitch** (`Brazo` → `Muñeca`) | **MG90S #1** | `90°` |
| **`CH4`** | `joint_5` (`J5`) | **Wrist Roll** (`Muñeca` → `Base de la garra`) | **MG90S #2** | `90°` |
| **`CH5`** | `gripper` (`J6`) | **Gripper Jaws** (`Engranaje1/2` → `Pinza1/2`) | **MG90S #3** | `90°` (`115°` Open / `65°` Closed) |

---

## 5. Step 4 — Flash the ESP32 & Center Servos Before Screwing Horns

1. Open [esp32_arm_v1_firmware.ino](file:///home/ishan/devotics_arm_v1_ws/src/devotics_arm_v1/firmware/ros_bridge/esp32_arm_v1_firmware/esp32_arm_v1_firmware.ino) in **Arduino IDE**.
2. Install the library **`Adafruit PWM Servo Driver Library`** via *Sketch → Include Library → Manage Libraries*.
3. Make sure line 24 has:
   ```cpp
   #define USE_PCA9685 1
   ```
4. Select your **ESP32 board** and port (`/dev/ttyUSB0`), and click **Upload**.
5. **Mechanical Zeroing (`90°` Alignment):**
   - When the ESP32 boots and the 12V SMPS is turned on, the firmware automatically sets all 6 channels (`CH0..CH5`) to **`90°` (`HOME`)**.
   - With the servos holding `90°`, attach the plastic servo horns so that the physical arm matches the **RViz Home Pose**:
     - **J1 (`Base`):** Facing straight forward
     - **J2 (`Antebrazo`):** Pointing straight up vertically (`90°` to the table)
     - **J3 (`Brazo`):** Pointing straight forward horizontally
     - **J4 (`Muñeca`):** Pointing straight forward horizontally
     - **J5 (`Base de la garra`):** Level / flat horizontally
     - **J6 (`Pinza1/2`):** Half-open neutral position

---

## 6. Step 5 — Test Individual Joints via Serial Monitor (Optional Sanity Check)

Before running MoveIt 2, you can open the **Arduino Serial Monitor** at **`115200` baud** (with line ending set to **Newline**) and test each joint smoothly:

- Type `PING` $\longrightarrow$ ESP32 replies `PONG`
- Type `J1 110` $\longrightarrow$ Base rotates smoothly to `110°`
- Type `J1 90` $\longrightarrow$ Base returns to `90°`
- Type `J6 115` $\longrightarrow$ Gripper opens
- Type `J6 65` $\longrightarrow$ Gripper closes
- Type `HOME` $\longrightarrow$ All 6 servos ramp smoothly back to `90°`

*(Close the Arduino Serial Monitor before starting the ROS 2 bridge so `/dev/ttyUSB0` is free!)*

---

## 7. Step 6 — Run MoveIt 2 + Physical ESP32 Arm + Pick-and-Place

Open **3 terminals** on your Ubuntu machine:

### Terminal 1: Launch MoveIt 2 & RViz
```bash
cd ~/devotics_arm_v1_ws/src/devotics_arm_v1
./moveit_launch.sh
```

### Terminal 2: Launch the ESP32 Physical Hardware Bridge
*(Check your USB port with `ls /dev/ttyUSB* /dev/ttyACM*`; if you get a permission error, run `sudo chmod 666 /dev/ttyUSB0` once).*
```bash
cd ~/devotics_arm_v1_ws/src/devotics_arm_v1
source install/setup.bash
ros2 run devotics_arm_moveit_config esp32_bridge.py --port /dev/ttyUSB0
```
Now, whenever you drag the interactive marker in RViz and click **"Plan & Execute"**, the physical arm will move in sync with RViz!

### Terminal 3: Run Autonomous Pick-and-Place
```bash
cd ~/devotics_arm_v1_ws/src/devotics_arm_v1
source install/setup.bash
ros2 run devotics_arm_moveit_config pick_and_place.py
```
*(Or add `--loop` for continuous pick-and-place cycles!)*

---

## 8. Fine-Tuning Direction or Offsets
If any physical joint rotates in the **opposite direction** of RViz or needs a few degrees of zero-trim:
1. Open [esp32_calibration.yaml](file:///home/ishan/devotics_arm_v1_ws/src/devotics_arm_v1/devotics_arm_moveit_config/config/esp32_calibration.yaml).
2. Flip `direction: 1` $\longleftrightarrow$ `direction: -1` (or adjust `offset_deg: 0.0`).
3. Rebuild the config:
   ```bash
   cd ~/devotics_arm_v1_ws/src/devotics_arm_v1
   colcon build --packages-select devotics_arm_moveit_config --allow-overriding devotics_arm_moveit_config
   ```
