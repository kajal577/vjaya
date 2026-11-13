#ifndef CONFIG_H
#define CONFIG_H

// L298N motor driver pins
#define IN1 8
#define IN2 9
#define IN3 10
#define IN4 11

// HC-05 Bluetooth pins
#define BT_RX 2   // Arduino receives from HC-05 TX
#define BT_TX 3   // Arduino sends to HC-05 RX

// Stop motors if no command is received
#define MOTOR_TIMEOUT 1500

#endif