#include "mpu6050.h"
#include "balance_config.h"
#include <Wire.h>
#include <math.h>

bool MPU6050Sensor::begin() {
  Wire.begin();
  Wire.setClock(400000);

  Wire.beginTransmission(MPU6050_ADDRESS);
  Wire.write(0x6B);
  Wire.write(0x00); // Wake MPU6050
  if (Wire.endTransmission() != 0) return false;

  // Gyroscope: +/- 250 degrees/second
  Wire.beginTransmission(MPU6050_ADDRESS);
  Wire.write(0x1B);
  Wire.write(0x00);
  if (Wire.endTransmission() != 0) return false;

  // Accelerometer: +/- 2g
  Wire.beginTransmission(MPU6050_ADDRESS);
  Wire.write(0x1C);
  Wire.write(0x00);
  if (Wire.endTransmission() != 0) return false;

  delay(100);
  return readRegisters();
}

bool MPU6050Sensor::readRegisters() {
  Wire.beginTransmission(MPU6050_ADDRESS);
  Wire.write(0x3B);

  if (Wire.endTransmission(false) != 0) return false;

  if (Wire.requestFrom(MPU6050_ADDRESS, 14) != 14) {
    return false;
  }

  ax = (Wire.read() << 8) | Wire.read();
  ay = (Wire.read() << 8) | Wire.read();
  az = (Wire.read() << 8) | Wire.read();

  Wire.read();
  Wire.read(); // Temperature

  gx = (Wire.read() << 8) | Wire.read();
  gy = (Wire.read() << 8) | Wire.read();
  gz = (Wire.read() << 8) | Wire.read();

  return true;
}

bool MPU6050Sensor::readRaw() {
  return readRegisters();
}

void MPU6050Sensor::calibrateGyro() {
  long total = 0;
  const int samples = 1000;

  Serial.println("Keep robot still and upright!");

  for (int i = 0; i < samples; i++) {
    if (readRegisters()) total += gy;
    delay(3);
  }

  gyroYOffset = (float)total / samples;
  Serial.println("Gyro calibration complete");
}

void MPU6050Sensor::updateAngle(float dt) {
  // Assumes the robot tilts around the MPU6050 Y axis.
  float accelAngle = atan2((float)ax, (float)az)
                     * 180.0f / PI;

  gyroRate = ((float)gy - gyroYOffset) / 131.0f;

  angle = COMPLEMENTARY_ALPHA * (angle + gyroRate * dt)
        + (1.0f - COMPLEMENTARY_ALPHA) * accelAngle;
}