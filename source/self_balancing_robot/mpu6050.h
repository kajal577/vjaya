#pragma once
#include <Arduino.h>

class MPU6050Sensor {
public:
  bool begin();
  bool readRaw();
  void calibrateGyro();
  void updateAngle(float dt);

  float angle = 0.0f;
  float gyroRate = 0.0f;

private:
  int16_t ax, ay, az;
  int16_t gx, gy, gz;
  float gyroYOffset = 0.0f;

  bool readRegisters();
};