
#ifndef FLEX_SENSOR_H
#define FLEX_SENSOR_H

#include <Arduino.h>

void initFlexSensors();

int readFlexSensor(uint8_t fingerIndex);

#endif
