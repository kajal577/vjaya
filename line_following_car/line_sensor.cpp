#include <Arduino.h>
#include "config.h"
#include "line_sensor.h"

void initLineSensors() {
    pinMode(LEFT_SENSOR, INPUT);
    pinMode(RIGHT_SENSOR, INPUT);
}

bool leftLineDetected() {
    return digitalRead(LEFT_SENSOR) == LINE_DETECTED;
}

bool rightLineDetected() {
    return digitalRead(RIGHT_SENSOR) == LINE_DETECTED;
}