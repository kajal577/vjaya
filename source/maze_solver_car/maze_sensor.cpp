#include <Arduino.h>
#include <Servo.h>
#include "maze_sensor.h"

#define TRIG_PIN 11
#define ECHO_PIN 12
#define SERVO_PIN 3

Servo scanner;

int measureDistance() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(3);

  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);

  digitalWrite(TRIG_PIN, LOW);

  unsigned long duration =
      pulseIn(ECHO_PIN, HIGH, 25000);

  if (duration == 0) {
    return 300;
  }

  int distance = duration * 0.0343 / 2;

  return distance;
}

void initSensor() {
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  scanner.attach(SERVO_PIN);

  scanner.write(90);
  delay(500);
}

MazeDistances scanMaze() {
  MazeDistances d;

  // Look left
  scanner.write(150);
  delay(300);
  d.left = measureDistance();

  // Look forward
  scanner.write(90);
  delay(300);
  d.front = measureDistance();

  // Look right
  scanner.write(30);
  delay(300);
  d.right = measureDistance();

  // Return to forward position
  scanner.write(90);
  delay(150);

  return d;
}