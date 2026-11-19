
#ifndef SERVO_CONTROL_H
#define SERVO_CONTROL_H

#include <Arduino.h>

void initServos();
void setServoAngle(uint8_t channel, int angle);
void moveServoSmooth(uint8_t channel, int targetAngle, int stepDelay);
void setAllServos(int angle);
void disableServos();

#endif
