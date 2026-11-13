#ifndef CONFIG_H
#define CONFIG_H

// L298N motor driver
#define IN1 8
#define IN2 9
#define IN3 10
#define IN4 11

// HC-SR04 ultrasonic sensor
#define TRIG_PIN 6
#define ECHO_PIN 7

// SG90 servo
#define SERVO_PIN 5

// Robot settings
#define OBSTACLE_DISTANCE 25
#define SAFE_DISTANCE 30
#define MOTOR_TURN_TIME 450
#define MOTOR_REVERSE_TIME 300

#endif