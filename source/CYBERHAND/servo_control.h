
#ifndef SERVO_CONTROL_H
#define SERVO_CONTROL_H

#include <Arduino.h>

void initServoControl();

void moveFinger(uint8_t fingerIndex, int sensorValue);

#endif
