#include "config.h"

#include "motor_control.h"
#include "gps_navigation.h"
#include "compass_control.h"
#include "bluetooth_control.h"
#include "obstacle_sensor.h"
#include "navigator.h"

void setup() {

  Serial.begin(9600);

  Serial.println("====================");
  Serial.println("GPS NAVIGATION CAR");
  Serial.println("====================");

  initMotors();

  initGPS();

  initCompass();

  initBluetooth();

  initObstacleSensor();

  stopMotors();

  Serial.println("SYSTEM READY");
}

void loop() {

  // Update GPS continuously
  updateGPS();

  // Read phone commands
  double latitude = 0;
  double longitude = 0;

  BTCommand command = readBluetoothCommand(
    latitude,
    longitude
  );

  if (command == BT_DESTINATION) {

    setDestination(latitude, longitude);
  }

  else if (command == BT_STOP) {

    cancelNavigation();
  }

  // Run autonomous navigation
  updateNavigation();
}