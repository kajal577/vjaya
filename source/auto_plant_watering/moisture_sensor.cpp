#include <Arduino.h>
#include "config.h"
#include "moisture_sensor.h"

void initMoistureSensor() {
    pinMode(MOISTURE_SENSOR_PIN, INPUT);
    analogReadResolution(12);
    analogSetPinAttenuation(MOISTURE_SENSOR_PIN, ADC_11db);

    Serial.println("Moisture sensor initialized");
}

int readMoistureRaw() {
    long total = 0;

    for (int i = 0; i < MOISTURE_SAMPLE_COUNT; i++) {
        total += analogRead(MOISTURE_SENSOR_PIN);
        delay(5);
    }

    return total / MOISTURE_SAMPLE_COUNT;
}