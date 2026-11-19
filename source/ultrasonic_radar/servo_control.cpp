
#include <Arduino.h>
#include <Servo.h>

#include "config.h"
#include "servo_control.h"

static Servo radarServo;

void initServo() {
    radarServo.attach(SERVO_PIN);
    radarServo.write(SERVO_MIN_ANGLE);

    delay(500);
}

void moveServoTo(int angle) {
    angle = constrain(angle, SERVO_MIN_ANGLE, SERVO_MAX_ANGLE);

    radarServo.write(angle);
}
