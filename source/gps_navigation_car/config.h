#ifndef CONFIG_H
#define CONFIG_H

// GPS: AltSoftSerial on UNO
#define GPS_BAUD 9600

// Bluetooth
#define BT_RX 2
#define BT_TX 3
#define BT_BAUD 9600

// L298N motor driver
#define ENA 5
#define ENB 6

#define IN1 4
#define IN2 7
#define IN3 12
#define IN4 13

// HC-SR04
#define TRIG_PIN 10
#define ECHO_PIN 11

// Motor speed
#define MOTOR_SPEED 150

// Navigation
#define ARRIVAL_DISTANCE 5.0
#define OBSTACLE_DISTANCE 30

#define TURN_THRESHOLD 20
#define GPS_TIMEOUT 3000

// Compass magnetic declination.
// Set these for your actual test location after checking
// the local magnetic declination.
#define DECLINATION_DEGREES 0
#define DECLINATION_MINUTES 0

#endif