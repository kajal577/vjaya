
#include <Arduino.h>
#include <SoftwareSerial.h>

#include "config.h"
#include "motor.h"
#include "bluetooth.h"

SoftwareSerial bluetoothSerial(BT_RX, BT_TX);

unsigned long lastCommandTime = 0;
char currentCommand = 'S';

void initBluetooth() {
    bluetoothSerial.begin(BT_BAUDRATE);

    lastCommandTime = millis();

    Serial.println("Bluetooth initialized");
}

void processBluetooth() {
    while (bluetoothSerial.available()) {
        char command = bluetoothSerial.read();

        // Ignore line endings and spaces
        if (command == '\n' ||
            command == '\r' ||
            command == ' ') {
            continue;
        }

        // Support lowercase commands too
        if (command >= 'a' && command <= 'z') {
            command -= 32;
        }

        switch (command) {
            case 'F':
                moveForward();
                currentCommand = 'F';
                break;

            case 'B':
                moveBackward();
                currentCommand = 'B';
                break;

            case 'L':
                turnLeft();
                currentCommand = 'L';
                break;

            case 'R':
                turnRight();
                currentCommand = 'R';
                break;

            case 'S':
                stopMotors();
                currentCommand = 'S';
                break;

            default:
                // Unknown command: stop for safety
                stopMotors();
                currentCommand = 'S';
                break;
        }

        lastCommandTime = millis();

        Serial.print("Bluetooth command: ");
        Serial.println(command);
    }

    // Automatic safety stop
    if (currentCommand != 'S' &&
        millis() - lastCommandTime > MOTOR_TIMEOUT) {

        stopMotors();
        currentCommand = 'S';

        Serial.println("Safety stop: command timeout");
    }
}
