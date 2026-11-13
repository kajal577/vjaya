#include <Arduino.h>
#include "config.h"
#include "ultrasonic.h"

void initUltrasonic() {
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);

    digitalWrite(TRIG_PIN, LOW);
}

int getDistance() {
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);

    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);

    digitalWrite(TRIG_PIN, LOW);

    unsigned long duration = pulseIn(
        ECHO_PIN,
        HIGH,
        30000
    );

    if (duration == 0) {
        return 400;
    }

    int distance = duration * 0.0343 / 2;

    return distance;
}