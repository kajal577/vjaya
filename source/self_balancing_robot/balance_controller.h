#pragma once
#include <Arduino.h>

void resetPID();
int calculateBalanceOutput(
  float angle,
  float gyroRate,
  float targetAngle,
  float dt
);