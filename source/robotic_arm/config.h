
#ifndef CONFIG_H
#define CONFIG_H

#include <Arduino.h>

// ==========================================
// ROBOTIC ARM CONFIGURATION
// Controller: Arduino UNO
// ==========================================

#define TOTAL_SERVOS 5

#define SERIAL_BAUD_RATE 9600

// ------------------------------------------
// JOYSTICK 1 PINS
// ------------------------------------------

#define JOY1_X_PIN A0
#define JOY1_Y_PIN A1

// ------------------------------------------
// JOYSTICK 2 PINS
// ------------------------------------------

#define JOY2_X_PIN A2
#define JOY2_Y_PIN A3
#define JOY2_SW_PIN 2

// ------------------------------------------
// SERVO MOTOR PINS
// ------------------------------------------

static const uint8_t SERVO_PINS[TOTAL_SERVOS] = {
    3,  // Base
    5,  // Shoulder
    6,  // Elbow
    9,  // Wrist
    10  // Gripper
};

// ------------------------------------------
// SERVO NAMES
// ------------------------------------------

static const char* const SERVO_NAMES[TOTAL_SERVOS] = {
    "Base",
    "Shoulder",
    "Elbow",
    "Wrist",
    "Gripper"
};

// ------------------------------------------
// SERVO ANGLE LIMITS
// Adjust after mechanical assembly.
// ------------------------------------------

static const int SERVO_MIN_ANGLE[TOTAL_SERVOS] = {
    0, 20, 20, 0, 20
};

static const int SERVO_MAX_ANGLE[TOTAL_SERVOS] = {
    180, 160, 160, 180, 90
};

// ------------------------------------------
// JOYSTICK SETTINGS
// ------------------------------------------

#define JOYSTICK_CENTER 512
#define JOYSTICK_DEADZONE 40

// Joystick movement speed
#define SERVO_STEP 2

// Gripper positions
#define GRIPPER_OPEN_ANGLE 20
#define GRIPPER_CLOSE_ANGLE 90

#endif