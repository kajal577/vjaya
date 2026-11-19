
#ifndef CONFIG_H
#define CONFIG_H

// Servo motor
#define SERVO_PIN 6

// HC-SR04 ultrasonic sensor
#define TRIG_PIN 9
#define ECHO_PIN 10

// Radar scanning angles
#define SERVO_MIN_ANGLE 0
#define SERVO_MAX_ANGLE 180
#define SERVO_STEP 2

// Timing
#define SERVO_SETTLE_MS 30
#define ULTRASONIC_TIMEOUT 30000UL

// Distance settings
#define MAX_DISTANCE_CM 400.0

// Serial communication
#define SERIAL_BAUD_RATE 9600

#endif
