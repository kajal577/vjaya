
#ifndef CONFIG_H
#define CONFIG_H

// L298N motor driver pins
#define IN1 8
#define IN2 9
#define IN3 10
#define IN4 11

// HC-05 Bluetooth pins
// HC-05 TXD -> Arduino D2
// Arduino D3 -> HC-05 RXD through voltage divider
#define BT_RX 2
#define BT_TX 3

// Bluetooth baud rate
#define BT_BAUDRATE 9600

// Stop motors if command is not refreshed
#define MOTOR_TIMEOUT 1500

#endif
