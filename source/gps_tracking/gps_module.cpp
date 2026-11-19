#include "gps_module.h"
#include "config.h"
#include <TinyGPSPlus.h>

TinyGPSPlus gps;
HardwareSerial gpsSerial(2);

void initGPS() {
    gpsSerial.begin(
        GPS_BAUD_RATE,
        SERIAL_8N1,
        GPS_RX_PIN,
        GPS_TX_PIN
    );

    Serial.println("GPS module initialized");
}

void updateGPS(GPSData &data) {

    while (gpsSerial.available()) {
        gps.encode(gpsSerial.read());
    }

    data.locationValid =
        gps.location.isValid() &&
        gps.location.age() < 3000;

    data.altitudeValid =
        gps.altitude.isValid() &&
        gps.altitude.age() < 3000;

    data.satellitesValid =
        gps.satellites.isValid() &&
        gps.satellites.age() < 3000;

    if (data.locationValid) {
        data.latitude = gps.location.lat();
        data.longitude = gps.location.lng();
    }

    if (data.altitudeValid) {
        data.altitude = gps.altitude.meters();
    }

    if (data.satellitesValid) {
        data.satellites = gps.satellites.value();
    }
}