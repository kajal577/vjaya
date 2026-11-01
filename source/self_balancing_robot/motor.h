#pragma once
#include <Arduino.h>

void initMotors();
void setMotors(int leftPower, int rightPower);
void stopMotors();