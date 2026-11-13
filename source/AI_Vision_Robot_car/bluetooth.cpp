#include <Arduino.h>
#include <SoftwareSerial.h>

#include "config.h"
#include "motor.h"
#include "bluetooth.h"

SoftwareSerial bluetooth(BT_RX, BT_TX);

unsigned long lastCommandTime = 0;

void initBluetooth() {
  bluetooth.begin(9600);
  lastCommandTime = millis();
}

void processBluetooth() {
  if (bluetooth.available()) {
    char command = bluetooth.read();

    lastCommandTime = millis();

    switch (command) {
      case 'F':
        moveForward();
        break;

      case 'B':
        moveBackward();
        break;

      case 'L':
        turnLeft();
        break;

      case 'R':
        turnRight();
        break;

      case 'S':
        stopMotors();
        break;

      default:
        stopMotors();
        break;
    }
  }

  // Automatic safety stop
  if (millis() - lastCommandTime > MOTOR_TIMEOUT) {
    stopMotors();
  }
}