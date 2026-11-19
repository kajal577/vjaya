#ifndef CONFIG_H
#define CONFIG_H

// ESP32 pin configuration
#define MOISTURE_SENSOR_PIN 34
#define PUMP_RELAY_PIN 26

// Relay configuration
// Change to false if your relay is HIGH-level triggered.
const bool RELAY_ACTIVE_LOW = true;

// Initial moisture thresholds (12-bit ADC: 0–4095)
// Typical capacitive sensors read higher when soil is dry.
// These values MUST be calibrated for your sensor.
const int SOIL_DRY_THRESHOLD = 2800;
const int SOIL_WET_THRESHOLD = 1800;

// Pump safety settings
const unsigned long MAX_PUMP_RUNTIME_MS = 15000UL;
const unsigned long MIN_PUMP_OFF_TIME_MS = 30000UL;

// Sensor settings
const int MOISTURE_SAMPLE_COUNT = 10;
const unsigned long SENSOR_READ_INTERVAL_MS = 1000UL;

#endif