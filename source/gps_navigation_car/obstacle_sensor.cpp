#include <Arduino.h>

#include "config.h"
#include "obstacle_sensor.h"

void initObstacleSensor() {

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  digitalWrite(TRIG_PIN, LOW);
}

int getObstacleDistance() {

  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);

  digitalWrite(TRIG_PIN, LOW);

  unsigned long duration = pulseIn(
    ECHO_PIN,
    HIGH,
    18000
  );

  if (duration == 0) {

    return 300;
  }

  return duration * 0.0343 / 2;
}