#ifndef MOTOR_H
#define MOTOR_H

#include <Arduino.h>

// =====================================================
// FAN RELAY INITIALIZATION
// =====================================================

void initMotors();

// =====================================================
// FAN 1
// =====================================================

void turnFan1On();
void turnFan1Off();

// =====================================================
// FAN 2
// =====================================================

void turnFan2On();
void turnFan2Off();

// =====================================================
// BOTH FANS
// =====================================================

void turnBothFansOn();
void turnBothFansOff();

// =====================================================
// OLD SINGLE-FAN COMMANDS
// =====================================================

void turnFanOn();
void turnFanOff();

// =====================================================
// BACKWARD COMPATIBILITY
// =====================================================

void stopMotors();
void moveForward();
void moveBackward();
void turnLeft();
void turnRight();

#endif