#include <Arduino.h>
#include "config.h"
#include "pump_control.h"

static bool pumpRunning = false;
static bool safetyLockout = false;

static unsigned long pumpStartTime = 0;
static unsigned long lastPumpStopTime = 0;

static void switchPump(bool state) {
    if (state) {
        digitalWrite(
            PUMP_RELAY_PIN,
            RELAY_ACTIVE_LOW ? LOW : HIGH
        );
    } else {
        digitalWrite(
            PUMP_RELAY_PIN,
            RELAY_ACTIVE_LOW ? HIGH : LOW
        );
    }

    pumpRunning = state;

    if (state) {
        pumpStartTime = millis();
        Serial.println("PUMP: ON");
    } else {
        lastPumpStopTime = millis();
        Serial.println("PUMP: OFF");
    }
}

void initPump() {
    // Set the output OFF before starting operation.
    digitalWrite(
        PUMP_RELAY_PIN,
        RELAY_ACTIVE_LOW ? HIGH : LOW
    );

    pinMode(PUMP_RELAY_PIN, OUTPUT);

    pumpRunning = false;
    safetyLockout = false;

    // Allow the first watering cycle immediately.
    lastPumpStopTime = millis() - MIN_PUMP_OFF_TIME_MS;

    Serial.println("Pump control initialized");
    Serial.println("Pump is OFF");
}

void updatePump(bool wateringRequired) {
    unsigned long currentTime = millis();

    // Stop the pump if the maximum runtime is reached.
    if (pumpRunning &&
        currentTime - pumpStartTime >= MAX_PUMP_RUNTIME_MS) {

        switchPump(false);
        safetyLockout = true;

        Serial.println("SAFETY: Maximum pump runtime reached");
        Serial.println("Watering locked until soil becomes wet");
        return;
    }

    // Reset safety lockout after the soil becomes sufficiently wet.
    if (!wateringRequired) {
        safetyLockout = false;
    }

    // Stop the pump when watering is no longer required.
    if (pumpRunning && !wateringRequired) {
        switchPump(false);
        return;
    }

    // Start the pump if the soil is dry and safety conditions allow it.
    if (!pumpRunning &&
        wateringRequired &&
        !safetyLockout &&
        currentTime - lastPumpStopTime >= MIN_PUMP_OFF_TIME_MS) {

        switchPump(true);
    }
}

bool isPumpRunning() {
    return pumpRunning;
}