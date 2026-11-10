#ifndef CONFIG_H
#define CONFIG_H

// L298N motor driver
#define IN1 8
#define IN2 9
#define IN3 10
#define IN4 11

// IR line sensors
#define LEFT_SENSOR 2
#define RIGHT_SENSOR 3

// Sensor calibration
// Change to HIGH if your sensors detect black with HIGH
#define LINE_DETECTED LOW

// Motor movement tuning
#define TURN_DELAY 10
#define SEARCH_DELAY 10

#endif