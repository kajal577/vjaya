#include <Arduino.h>
#include <Wire.h>
#include <QMC5883LCompass.h>

#include "compass_control.h"
#include "config.h"

static QMC5883LCompass compass;

void initCompass() {

  Wire.begin();

  compass.init();

  compass.setMagneticDeclination(
    DECLINATION_DEGREES,
    DECLINATION_MINUTES
  );

  compass.setSmoothing(5, true);

  Serial.println("COMPASS INITIALIZED");
}

int getHeading() {

  compass.read();

  return compass.getAzimuth();
}