
#include <Arduino.h>

#include "config.h"
#include "ultrasonic.h"

void initUltrasonic() {
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);

    digitalWrite(TRIG_PIN, LOW);
}

float readDistanceCm() {
    // Send ultrasonic trigger pulse
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);

    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);

    digitalWrite(TRIG_PIN, LOW);

    // Measure echo duration
    unsigned long duration = pulseIn(
        ECHO_PIN,
        HIGH,
        ULTRASONIC_TIMEOUT
    );

    // No echo received
    if (duration == 0) {
        return -1.0;
    }

    // Convert echo time into distance
    float distance = (duration * 0.0343) / 2.0;

    // Reject readings outside sensor range
    if (distance <= 0 || distance > MAX_DISTANCE_CM) {
        return -1.0;
    }

    return distance;
}
