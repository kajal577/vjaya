
#include <Arduino.h>

#include "config.h"
#include "flex_sensor.h"
#include "servo_control.h"

void setup() {
    Serial.begin(SERIAL_BAUD_RATE);
    delay(500);

    Serial.println();
    Serial.println("==============================");
    Serial.println("   CYBERHAND ROBOTIC HAND");
    Serial.println("==============================");

    initFlexSensors();
    Serial.println("Flex sensors initialized.");

    initServoControl();
    Serial.println("Servo motors initialized.");

    Serial.println("CYBERHAND READY");
}

void loop() {
    for (uint8_t i = 0; i < TOTAL_FINGERS; i++) {
        int sensorValue = readFlexSensor(i);

        moveFinger(i, sensorValue);

        Serial.print(FINGER_NAMES[i]);
        Serial.print(" | Sensor: ");
        Serial.print(sensorValue);

        Serial.println();
    }

    Serial.println("------------------------------");
    delay(20);
}
