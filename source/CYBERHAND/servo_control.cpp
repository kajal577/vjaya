
#include "servo_control.h"
#include "config.h"

#include <ESP32Servo.h>

// Create five servo objects
static Servo fingerServos[TOTAL_FINGERS];

void initServoControl() {

    for (uint8_t i = 0; i < TOTAL_FINGERS; i++) {

        fingerServos[i].setPeriodHertz(50);

        fingerServos[i].attach(
            SERVO_PINS[i],
            500,
            2400
        );

        fingerServos[i].write(SERVO_STRAIGHT_ANGLE);
    }
}

void moveFinger(uint8_t fingerIndex, int sensorValue) {

    if (fingerIndex >= TOTAL_FINGERS) {
        return;
    }

    int straightValue = FLEX_STRAIGHT_VALUE[fingerIndex];
    int bentValue = FLEX_BENT_VALUE[fingerIndex];

    if (straightValue == bentValue) {
        return;
    }

    // Convert sensor reading into servo angle
    int servoAngle = map(
        sensorValue,
        straightValue,
        bentValue,
        SERVO_STRAIGHT_ANGLE,
        SERVO_BENT_ANGLE
    );

    // Keep angle within safe limits
    servoAngle = constrain(
        servoAngle,
        SERVO_MIN_ANGLE,
        SERVO_MAX_ANGLE
    );

    fingerServos[fingerIndex].write(servoAngle);
}
