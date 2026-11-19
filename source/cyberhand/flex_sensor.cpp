
#include "flex_sensor.h"
#include "config.h"

void initFlexSensors() {

    analogReadResolution(12);

    for (uint8_t i = 0; i < TOTAL_FINGERS; i++) {
        pinMode(FLEX_SENSOR_PINS[i], INPUT);

        analogSetPinAttenuation(
            FLEX_SENSOR_PINS[i],
            ADC_11db
        );
    }
}

int readFlexSensor(uint8_t fingerIndex) {

    if (fingerIndex >= TOTAL_FINGERS) {
        return 0;
    }

    long total = 0;

    // Average five ADC readings
    for (uint8_t i = 0; i < 5; i++) {
        total += analogRead(FLEX_SENSOR_PINS[fingerIndex]);
        delayMicroseconds(500);
    }

    return total / 5;
}
