
#ifndef CONFIG_H
#define CONFIG_H

#include <Arduino.h>

// Number of fingers
#define TOTAL_FINGERS 5

// Serial Monitor
#define SERIAL_BAUD_RATE 115200

// Flex sensor pins
static const uint8_t FLEX_SENSOR_PINS[TOTAL_FINGERS] = {
    32,  // Thumb
    33,  // Index
    34,  // Middle
    35,  // Ring
    36   // Little
};

// Servo signal pins
static const uint8_t SERVO_PINS[TOTAL_FINGERS] = {
    13,  // Thumb
    14,  // Index
    16,  // Middle
    17,  // Ring
    18   // Little
};

// Finger names
static const char* const FINGER_NAMES[TOTAL_FINGERS] = {
    "Thumb",
    "Index",
    "Middle",
    "Ring",
    "Little"
};

// Initial flex sensor calibration values.
// Replace these after testing straight and bent sensor readings.
static const int FLEX_STRAIGHT_VALUE[TOTAL_FINGERS] = {
    1500, 1500, 1500, 1500, 1500
};

static const int FLEX_BENT_VALUE[TOTAL_FINGERS] = {
    3000, 3000, 3000, 3000, 3000
};

// Servo angle limits
#define SERVO_MIN_ANGLE 0
#define SERVO_MAX_ANGLE 180

// Servo positions
#define SERVO_STRAIGHT_ANGLE 0
#define SERVO_BENT_ANGLE 180

#endif
