#include "config.h"
#include "gps_module.h"
#include "display.h"

GPSData gpsData = {};

unsigned long previousDisplayUpdate = 0;

void setup() {

    Serial.begin(SERIAL_BAUD_RATE);

    Serial.println();
    Serial.println("GPS TRACKING SYSTEM");
    Serial.println("-------------------");

    initDisplay();
    initGPS();

    Serial.println("System ready");
}

void loop() {

    updateGPS(gpsData);

    if (millis() - previousDisplayUpdate >= DISPLAY_UPDATE_INTERVAL) {

        previousDisplayUpdate = millis();

        updateDisplay(gpsData);

        if (gpsData.locationValid) {

            Serial.print("Latitude: ");
            Serial.println(gpsData.latitude, 6);

            Serial.print("Longitude: ");
            Serial.println(gpsData.longitude, 6);

            if (gpsData.altitudeValid) {
                Serial.print("Altitude: ");
                Serial.print(gpsData.altitude);
                Serial.println(" m");
            }

            if (gpsData.satellitesValid) {
                Serial.print("Satellites: ");
                Serial.println(gpsData.satellites);
            }

            Serial.println("-------------------");
        } else {
            Serial.println("Waiting for GPS signal...");
        }
    }
}