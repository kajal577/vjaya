#include <Arduino.h>
#include <AltSoftSerial.h>
#include <TinyGPS++.h>

#include "gps_navigation.h"
#include "config.h"

static AltSoftSerial gpsSerial;
static TinyGPSPlus gps;

void initGPS() {

  gpsSerial.begin(GPS_BAUD);

  Serial.println("GPS INITIALIZED");
}

void updateGPS() {

  while (gpsSerial.available()) {

    gps.encode(gpsSerial.read());
  }
}

bool gpsAvailable() {

  return gps.location.isValid() &&
         gps.location.age() < GPS_TIMEOUT;
}

double getLatitude() {

  return gps.location.lat();
}

double getLongitude() {

  return gps.location.lng();
}

double getDistanceTo(
  double targetLat,
  double targetLon
) {

  return TinyGPSPlus::distanceBetween(
    getLatitude(),
    getLongitude(),
    targetLat,
    targetLon
  );
}

double getBearingTo(
  double targetLat,
  double targetLon
) {

  return TinyGPSPlus::courseTo(
    getLatitude(),
    getLongitude(),
    targetLat,
    targetLon
  );
}