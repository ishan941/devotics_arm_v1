/*
 * ============================================================================
 * Devotics Arm V1 — ESP32 Servo Controller Firmware (ROS 2 / MoveIt 2 Bridge)
 * ============================================================================
 * Supports:
 *   1. PCA9685 16-Channel I2C PWM Driver (Default: USE_PCA9685 = 1)
 *      OR Direct ESP32 GPIO PWM Pins (Set USE_PCA9685 = 0)
 *   2. USB Serial (115200 baud) AND Optional Wi-Fi TCP Server (port 8888)
 *   3. Smooth velocity ramping (prevents violent startup jerks on MG996R)
 *
 * Serial Command Protocol (115200 baud, newline '\n' terminated):
 *   - "S d1 d2 d3 d4 d5 d6\n" -> Set all 6 servos (J1..J5 + Gripper) in degrees
 *                                Example: "S 90 90 90 90 90 90\n"
 *   - "J1 90\n" .. "J6 110\n" -> Set single servo n (1..6) to angle in degrees
 *   - "HOME\n"                -> Return all servos smoothly to home angles
 *   - "PING\n"                -> Replies "PONG\n" and prints current angles
 * ============================================================================
 */

#include <Arduino.h>

// ----------------------------------------------------------------------------
// HARDWARE DRIVER SELECTION
// Set USE_PCA9685 to 1 if using PCA9685 I2C 16-ch driver (SDA=21, SCL=22)
// Set USE_PCA9685 to 0 if servos are wired directly to ESP32 GPIO pins
// ----------------------------------------------------------------------------
#define USE_PCA9685 0

// Optional Wi-Fi TCP Bridge (Set USE_WIFI to 1 and fill SSID/PASS if wireless)
#define USE_WIFI 1
const char* WIFI_SSID = "Devotics_2G";
const char* WIFI_PASS = "2858@2858";
const uint16_t TCP_PORT = 8888;

#if USE_PCA9685
  #include <Wire.h>
  #include <Adafruit_PWMServoDriver.h>
  Adafruit_PWMServoDriver pca = Adafruit_PWMServoDriver(0x40);
  // Pulse width range for MG996R / MG90S at 50Hz (out of 4096 ticks = 20,000 us)
  #define SERVO_MIN_US 500
  #define SERVO_MAX_US 2500
  const uint8_t SERVO_CHANNELS[6] = {0, 1, 2, 3, 4, 5}; // PCA9685 CH0 .. CH5
#else
  #include <ESP32Servo.h>
  Servo servos[6];
  // Direct ESP32 GPIO pin mapping (J1..J5, J6=Gripper)
  const uint8_t SERVO_PINS[6] = {25, 26, 27, 14, 12, 13};
#endif

#if USE_WIFI
  #include <WiFi.h>
  WiFiServer tcpServer(TCP_PORT);
  WiFiClient tcpClient;
#endif

// ----------------------------------------------------------------------------
// SERVO SAFETY LIMITS & SMOOTH RAMPING STATE
// ----------------------------------------------------------------------------
const int NUM_SERVOS = 6;
const float HOME_DEG[6] = {90.0f, 90.0f, 90.0f, 90.0f, 90.0f, 90.0f};
const float MIN_DEG[6]  = {10.0f, 15.0f, 15.0f, 15.0f,  0.0f, 40.0f};
const float MAX_DEG[6]  = {170.0f, 165.0f, 165.0f, 165.0f, 180.0f, 130.0f};

float currentDeg[6] = {90.0f, 90.0f, 90.0f, 90.0f, 90.0f, 90.0f};
float targetDeg[6]  = {90.0f, 90.0f, 90.0f, 90.0f, 90.0f, 90.0f};

// Maximum degrees change per 20ms update tick (~90 deg/sec smooth motion)
const float MAX_STEP_PER_TICK = 1.8f;
unsigned long lastUpdateMs = 0;

// ----------------------------------------------------------------------------
// LOW-LEVEL SERVO WRITE
// ----------------------------------------------------------------------------
void writeServoHardware(int idx, float deg) {
  deg = constrain(deg, MIN_DEG[idx], MAX_DEG[idx]);
  int us = (int)(SERVO_MIN_US + (deg / 180.0f) * (SERVO_MAX_US - SERVO_MIN_US));

#if USE_PCA9685
  // 50 Hz -> 20,000 us period over 4096 counts
  uint16_t ticks = (uint16_t)((us * 4096L) / 20000L);
  pca.setPWM(SERVO_CHANNELS[idx], 0, ticks);
#else
  servos[idx].writeMicroseconds(us);
#endif
}

// ----------------------------------------------------------------------------
// COMMAND PARSER
// ----------------------------------------------------------------------------
void processCommand(String line) {
  line.trim();
  if (line.length() == 0) return;

  if (line.equalsIgnoreCase("PING")) {
    Serial.println("PONG");
    return;
  }

  if (line.equalsIgnoreCase("HOME")) {
    for (int i = 0; i < NUM_SERVOS; i++) {
      targetDeg[i] = HOME_DEG[i];
    }
    Serial.println("OK HOME");
    return;
  }

  // Multi-servo packet: "S d1 d2 d3 d4 d5 d6"
  if (line.startsWith("S ") || line.startsWith("s ")) {
    float vals[6];
    int parsed = sscanf(
      line.c_str() + 2,
      "%f %f %f %f %f %f",
      &vals[0], &vals[1], &vals[2], &vals[3], &vals[4], &vals[5]
    );
    if (parsed == 6) {
      for (int i = 0; i < 6; i++) {
        targetDeg[i] = constrain(vals[i], MIN_DEG[i], MAX_DEG[i]);
      }
      Serial.println("OK S");
    }
    return;
  }

  // Single-servo command: "J1 90" .. "J6 110"
  if (line.startsWith("J") || line.startsWith("j")) {
    int jointIdx = -1;
    float degVal = 90.0f;
    if (sscanf(line.c_str() + 1, "%d %f", &jointIdx, &degVal) == 2) {
      if (jointIdx >= 1 && jointIdx <= NUM_SERVOS) {
        int i = jointIdx - 1;
        targetDeg[i] = constrain(degVal, MIN_DEG[i], MAX_DEG[i]);
        Serial.printf("OK J%d %.1f\n", jointIdx, targetDeg[i]);
      }
    }
    return;
  }
}

// ----------------------------------------------------------------------------
// SETUP & LOOP
// ----------------------------------------------------------------------------
void setup() {
  Serial.begin(115200);
  delay(200);

#if USE_PCA9685
  Wire.begin(21, 22);
  pca.begin();
  pca.setOscillatorFrequency(27000000);
  pca.setPWMFreq(50);
  delay(50);
#else
  ESP32PWM::allocateTimer(0);
  ESP32PWM::allocateTimer(1);
  ESP32PWM::allocateTimer(2);
  ESP32PWM::allocateTimer(3);
  for (int i = 0; i < NUM_SERVOS; i++) {
    servos[i].setPeriodHertz(50);
    servos[i].attach(SERVO_PINS[i], 500, 2500);
  }
#endif

  // Initialize all servos at HOME (90 deg)
  for (int i = 0; i < NUM_SERVOS; i++) {
    currentDeg[i] = HOME_DEG[i];
    targetDeg[i]  = HOME_DEG[i];
    writeServoHardware(i, currentDeg[i]);
  }

#if USE_WIFI
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(300);
  }
  tcpServer.begin();
  Serial.print("WiFi Ready IP: ");
  Serial.println(WiFi.localIP());
#endif

  Serial.println("READY Devotics Arm V1 ESP32 Firmware");
}

void loop() {
  // 1. Read USB Serial Commands
  while (Serial.available() > 0) {
    String line = Serial.readStringUntil('\n');
    processCommand(line);
  }

#if USE_WIFI
  // 2. Read Wi-Fi TCP Commands (if enabled)
  if (tcpServer.hasClient()) {
    if (!tcpClient || !tcpClient.connected()) {
      tcpClient = tcpServer.available();
    } else {
      tcpServer.available().stop();
    }
  }
  while (tcpClient && tcpClient.connected() && tcpClient.available() > 0) {
    String line = tcpClient.readStringUntil('\n');
    processCommand(line);
  }
#endif

  // 3. 50Hz Smooth Interpolation Loop (every 20 ms)
  unsigned long now = millis();
  if (now - lastUpdateMs >= 20) {
    lastUpdateMs = now;
    for (int i = 0; i < NUM_SERVOS; i++) {
      float diff = targetDeg[i] - currentDeg[i];
      if (fabs(diff) > 0.05f) {
        if (fabs(diff) <= MAX_STEP_PER_TICK) {
          currentDeg[i] = targetDeg[i];
        } else {
          currentDeg[i] += (diff > 0.0f ? MAX_STEP_PER_TICK : -MAX_STEP_PER_TICK);
        }
        writeServoHardware(i, currentDeg[i]);
      }
    }
  }
}
