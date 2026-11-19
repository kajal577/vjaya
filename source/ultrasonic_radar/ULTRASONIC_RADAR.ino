
#include "config.h"
#include "servo_control.h"
#include "ultrasonic.h"

void scanAtAngle(int angle);

void setup() {
    Serial.begin(SERIAL_BAUD_RATE);

    initServo();
    initUltrasonic();

    Serial.println("ULTRASONIC RADAR SYSTEM");
    Serial.println("Angle,Distance");
}

void loop() {
    // Scan from 0 to 180 degrees
    for (int angle = SERVO_MIN_ANGLE;
         angle <= SERVO_MAX_ANGLE;
         angle += SERVO_STEP) {

        scanAtAngle(angle);
    }

    // Scan back from 180 to 0 degrees
    for (int angle = SERVO_MAX_ANGLE;
         angle >= SERVO_MIN_ANGLE;
         angle -= SERVO_STEP) {

        scanAtAngle(angle);
    }
}

void scanAtAngle(int angle) {
    moveServoTo(angle);

    delay(SERVO_SETTLE_MS);

    float distance = readDistanceCm();

    Serial.print(angle);
    Serial.print(",");

    if (distance < 0) {
        Serial.println("No Echo");
    } else {
        Serial.println(distance);
    }
}
