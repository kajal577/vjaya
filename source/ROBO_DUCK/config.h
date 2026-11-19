
#ifndef CONFIG_H
#define CONFIG_H

// ESP32 I2C configuration
#define I2C_SDA 21
#define I2C_SCL 22

// PCA9685
#define PCA9685_ADDRESS 0x40
#define SERVO_FREQUENCY 50

// SG90 configuration
#define SERVO_COUNT 6

// Conservative initial pulse range.
// Calibrate each actual servo before increasing.
#define SERVO_MIN_US 1000
#define SERVO_MAX_US 2000

// Servo channels
#define LEFT_HIP_ROLL    0
#define LEFT_HIP_PITCH   1
#define LEFT_KNEE        2

#define RIGHT_HIP_ROLL   3
#define RIGHT_HIP_PITCH  4
#define RIGHT_KNEE       5

// Initial servo positions
#define SERVO_CENTER 90

// Movement settings
#define WALK_DELAY 20
#define WALK_STEP_TIME 800

// Software angle limits
#define SERVO_MIN_ANGLE 0
#define SERVO_MAX_ANGLE 180

#endif
