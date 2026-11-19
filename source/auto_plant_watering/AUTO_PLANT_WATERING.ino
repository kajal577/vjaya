#include <Arduino.h>

#include "config.h"
#include "moisture_sensor.h"
#include "pump_control.h"

bool wateringRequired = false;

unsigned long lastSensorReadTime = 0;

void setup() {
    Serial.begin(115200);
    delay(500);

    Serial.println();
    Serial.println("==============================");
    Serial.println(" AUTO PLANT WATERING SYSTEM");
    Serial.println("==============================");

    initMoistureSensor();
    initPump();

    Serial.println("System ready");
}

void loop() {
    unsigned long currentTime = millis();

    // Read soil moisture at regular intervals.
    if (currentTime - lastSensorReadTime >= SENSOR_READ_INTERVAL_MS) {
        lastSensorReadTime = currentTime;

        int moistureValue = readMoistureRaw();

        // Hysteresis: use separate dry and wet thresholds.
        if (!wateringRequired &&
            moistureValue >= SOIL_DRY_THRESHOLD) {
            wateringRequired = true;
        }
        else if (wateringRequired &&
                 moistureValue <= SOIL_WET_THRESHOLD) {
            wateringRequired = false;
        }

        Serial.print("Soil moisture raw value: ");
        Serial.println(moistureValue);

        Serial.print("Watering required: ");
        Serial.println(wateringRequired ? "YES" : "NO");

        Serial.println("------------------------------");
    }

    // Pump safety and automatic control.
    updatePump(wateringRequired);
}