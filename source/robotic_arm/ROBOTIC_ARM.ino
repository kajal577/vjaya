
/*
  Project: ROBOTIC ARM WITH GRIPPER
  Controller: Arduino UNO
  Control: Two Joystick Modules
  Motors: Five Servo Motors

  VJaYa Robotics
*/

#include <Arduino.h>

#include "config.h"
#include "joystick.h"
#include "servo_control.h"

// ==========================================
// SETUP
// ==========================================

void setup() {

    Serial.begin(SERIAL_BAUD_RATE);

    Serial.println("================================");
    Serial.println(" ROBOTIC ARM WITH GRIPPER");
    Serial.println(" Arduino UNO");
    Serial.println("================================");

    // Initialize joystick modules
    initJoystick();

    Serial.println("Joysticks initialized.");

    // Initialize servo motors
    initServoControl();

    Serial.println("Servo motors initialized.");

    Serial.println("ROBOTIC ARM READY");
}

// ==========================================
// MAIN LOOP
// ==========================================

void loop() {

    // Read joystick positions
    readJoystick();

    // Control robotic arm movements
    updateServoControl();

    delay(20);
}
