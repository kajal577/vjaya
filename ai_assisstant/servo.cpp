#include "servo.h"
#include <ESP32Servo.h>

#define SERVO_PIN 19

#define GATE_OPEN_ANGLE 120
#define GATE_CLOSE_ANGLE 0

Servo gateServo;

// =====================================================
// INITIALIZE SERVO
// =====================================================

void initServo()
{
    gateServo.setPeriodHertz(50);
    gateServo.attach(SERVO_PIN, 500, 2400);

    // Start with gate closed
    gateServo.write(GATE_CLOSE_ANGLE);

    Serial.println("==============================");
    Serial.println("GATE SERVO SYSTEM READY");
    Serial.println("Servo GPIO: 19");
    Serial.println("Gate: CLOSED");
    Serial.println("==============================");
}

// =====================================================
// GATE OPEN
// =====================================================

void gateOpen()
{
    gateServo.write(GATE_OPEN_ANGLE);

    Serial.println("GATE STATE: OPEN");
}

// =====================================================
// GATE CLOSE
// =====================================================

void gateClose()
{
    gateServo.write(GATE_CLOSE_ANGLE);

    Serial.println("GATE STATE: CLOSED");
}