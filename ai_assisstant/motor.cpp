#include "motor.h"
#include <Arduino.h>

// =====================================================
// 2-CHANNEL RELAY CONFIGURATION
// =====================================================

#define FAN1_RELAY_PIN 13
#define FAN2_RELAY_PIN 14

// Active LOW relay
#define RELAY_ON  LOW
#define RELAY_OFF HIGH

// =====================================================
// FAN 1
// =====================================================

void turnFan1On()
{
    digitalWrite(FAN1_RELAY_PIN, RELAY_ON);

    Serial.println("FAN 1 STATE: ON");
}

void turnFan1Off()
{
    digitalWrite(FAN1_RELAY_PIN, RELAY_OFF);

    Serial.println("FAN 1 STATE: OFF");
}

// =====================================================
// FAN 2
// =====================================================

void turnFan2On()
{
    digitalWrite(FAN2_RELAY_PIN, RELAY_ON);

    Serial.println("FAN 2 STATE: ON");
}

void turnFan2Off()
{
    digitalWrite(FAN2_RELAY_PIN, RELAY_OFF);

    Serial.println("FAN 2 STATE: OFF");
}

// =====================================================
// BOTH FANS
// =====================================================

void turnBothFansOn()
{
    turnFan1On();
    turnFan2On();

    Serial.println("BOTH FANS: ON");
}

void turnBothFansOff()
{
    turnFan1Off();
    turnFan2Off();

    Serial.println("BOTH FANS: OFF");
}

// =====================================================
// INITIALIZE FAN RELAYS
// =====================================================

void initMotors()
{
    pinMode(FAN1_RELAY_PIN, OUTPUT);
    pinMode(FAN2_RELAY_PIN, OUTPUT);

    // Start both fans OFF
    digitalWrite(FAN1_RELAY_PIN, RELAY_OFF);
    digitalWrite(FAN2_RELAY_PIN, RELAY_OFF);

    Serial.println("==============================");
    Serial.println("2-CHANNEL FAN RELAY SYSTEM READY");
    Serial.println("Fan 1 Relay: GPIO 13");
    Serial.println("Fan 2 Relay: GPIO 14");
    Serial.println("Fan 1: OFF");
    Serial.println("Fan 2: OFF");
    Serial.println("==============================");
}

// =====================================================
// OLD SINGLE-FAN FUNCTIONS
// =====================================================

void turnFanOn()
{
    turnFan1On();
}

void turnFanOff()
{
    turnFan1Off();
}

// =====================================================
// BACKWARD COMPATIBILITY
// =====================================================

void stopMotors()
{
    turnBothFansOff();
}

void moveForward()
{
    turnBothFansOn();
}

void moveBackward()
{
    turnBothFansOn();
}

void turnLeft()
{
    turnBothFansOn();
}

void turnRight()
{
    turnBothFansOn();
}