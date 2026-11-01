#include <Arduino.h>

#include "navigator.h"
#include "motor_control.h"
#include "maze_sensor.h"

#define OPEN_DISTANCE 25

#define FORWARD_TIME 180
#define TURN_90_TIME 400
#define TURN_180_TIME 800

void initNavigator() {
  initMotors();
  initSensor();

  stopMotors();

  Serial.println("MAZE SOLVER READY");
}

void navigateMaze() {

  MazeDistances d = scanMaze();

  Serial.print("LEFT: ");
  Serial.print(d.left);

  Serial.print(" FRONT: ");
  Serial.print(d.front);

  Serial.print(" RIGHT: ");
  Serial.println(d.right);

  // Priority 1: Turn left if possible
  if (d.left > OPEN_DISTANCE) {

    Serial.println("TURN LEFT");

    turnLeft();
    delay(TURN_90_TIME);

    stopMotors();
    delay(150);

    moveForward();
    delay(FORWARD_TIME);

    stopMotors();
  }

  // Priority 2: Move forward
  else if (d.front > OPEN_DISTANCE) {

    Serial.println("MOVE FORWARD");

    moveForward();
    delay(FORWARD_TIME);

    stopMotors();
  }

  // Priority 3: Turn right
  else if (d.right > OPEN_DISTANCE) {

    Serial.println("TURN RIGHT");

    turnRight();
    delay(TURN_90_TIME);

    stopMotors();
    delay(150);

    moveForward();
    delay(FORWARD_TIME);

    stopMotors();
  }

  // Priority 4: Dead end
  else {

    Serial.println("DEAD END - TURN AROUND");

    moveBackward();
    delay(250);

    turnRight();
    delay(TURN_180_TIME);

    stopMotors();
  }

  delay(100);
}