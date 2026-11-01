#include <Arduino.h>
#include "balance_config.h"
#include "mpu6050.h"
#include "motor.h"
#include "bluetooth_control.h"
#include "balance_controller.h"

MPU6050Sensor imu;

unsigned long lastLoop = 0;
bool wasArmed = false;

void setup() {
  Serial.begin(115200);

  initMotors();
  initBluetooth();

  Serial.println("Self-balancing robot starting");

  if (!imu.begin()) {
    Serial.println("ERROR: MPU6050 not detected!");
    while (true) {
      stopMotors();
      delay(100);
    }
  }

  // Keep robot upright and motionless during calibration.
  imu.calibrateGyro();

  if (!imu.readRaw()) {
    Serial.println("ERROR: MPU6050 read failed!");
    while (true) {
      stopMotors();
      delay(100);
    }
  }

  imu.updateAngle(0.005f);

  lastLoop = millis();
  Serial.println("Ready. Send A to arm, X to disarm.");
}

void loop() {
  readBluetooth();

  unsigned long now = millis();

  if (now - lastLoop < LOOP_PERIOD_MS) return;

  float dt = (now - lastLoop) / 1000.0f;
  lastLoop = now;

  // Prevent an unstable controller after a long delay.
  if (dt <= 0.0f || dt > 0.03f) {
    stopMotors();
    resetPID();
    return;
  }

  if (!imu.readRaw()) {
    stopMotors();
    resetPID();
    return;
  }

  imu.updateAngle(dt);

  if (!isArmed()) {
    stopMotors();
    resetPID();
    wasArmed = false;
    return;
  }

  if (!wasArmed) {
    resetPID();
    wasArmed = true;
  }

  float angle = imu.angle - BALANCE_ANGLE_OFFSET;

  // Falling too far: cut motor drive and require re-arming.
  if (abs(angle) > FALL_ANGLE_LIMIT) {
    stopMotors();
    resetPID();
    Serial.println("FALL DETECTED: send A after repositioning");
    // In this starter version, the next A command re-arms.
    // Send X, then A to reset the arm state.
    return;
  }

  char command = getMovementCommand();

  float targetAngle = 0.0f;
  int turn = 0;

  if (command == 'F') targetAngle = MOVE_ANGLE;
  if (command == 'B') targetAngle = -MOVE_ANGLE;
  if (command == 'L') turn = -TURN_POWER;
  if (command == 'R') turn = TURN_POWER;

  int balance = calculateBalanceOutput(
    angle, imu.gyroRate, targetAngle, dt
  );

  int left = balance + turn;
  int right = balance - turn;

  left = constrain(left, -MAX_MOTOR_POWER, MAX_MOTOR_POWER);
  right = constrain(right, -MAX_MOTOR_POWER, MAX_MOTOR_POWER);

  setMotors(left, right);

  // Keep serial output light to preserve loop timing.
  static unsigned long lastPrint = 0;
  if (now - lastPrint >= 250) {
    lastPrint = now;
    Serial.print("Angle: ");
    Serial.print(angle);
    Serial.print(" Command: ");
    Serial.println(command);
  }
}