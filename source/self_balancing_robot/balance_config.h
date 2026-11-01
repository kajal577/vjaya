#pragma once

// Arduino Uno pin configuration
#define MOTOR_ENA 5
#define MOTOR_IN1 7
#define MOTOR_IN2 8

#define MOTOR_ENB 6
#define MOTOR_IN3 9
#define MOTOR_IN4 4

#define BT_RX 10  // Arduino receives from HC-05 TX
#define BT_TX 11  // Arduino transmits to HC-05 RX

// Adjust these after checking motor directions.
#define LEFT_MOTOR_DIRECTION  1
#define RIGHT_MOTOR_DIRECTION 1

// MPU6050 settings
#define MPU6050_ADDRESS 0x68

// Complementary filter
#define COMPLEMENTARY_ALPHA 0.98f

// PID starting values only; they require real-world tuning.
#define PID_KP 18.0f
#define PID_KI 0.0f
#define PID_KD 0.8f

// Adjust the zero angle after mounting/calibration.
#define BALANCE_ANGLE_OFFSET 0.0f

// Movement targets; tune after balancing works.
#define MOVE_ANGLE 2.0f
#define TURN_POWER 35

#define MAX_MOTOR_POWER 180
#define FALL_ANGLE_LIMIT 35.0f
#define LOOP_PERIOD_MS 5