#include <Arduino.h>
#include <Servo.h>

#include "config.h"
#include "scanner.h"
#include "ultrasonic.h"

Servo scannerServo;

void initScanner() {
    scannerServo.attach(SERVO_PIN);

    scannerServo.write(90);
    delay(500);
}

int scanLeft() {
    scannerServo.write(150);
    delay(400);

    int distance = getDistance();

    scannerServo.write(90);
    delay(200);

    return distance;
}

int scanRight() {
    scannerServo.write(30);
    delay(400);

    int distance = getDistance();

    scannerServo.write(90);
    delay(200);

    return distance;
}

int scanFront() {
    scannerServo.write(90);
    delay(200);

    return getDistance();
}