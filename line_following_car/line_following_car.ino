#include "config.h"
#include "motor.h"
#include "line_sensor.h"

void setup() {
    Serial.begin(9600);

    initMotors();
    initLineSensors();

    Serial.println("Line Following Robot Started");

    delay(1000);
}

void loop() {
    bool leftDetected = leftLineDetected();
    bool rightDetected = rightLineDetected();

    Serial.print("Left: ");
    Serial.print(leftDetected);

    Serial.print(" | Right: ");
    Serial.println(rightDetected);

    // Both sensors detect the line
    if (leftDetected && rightDetected) {
        moveForward();
    }

    // Left sensor detects line
    else if (leftDetected && !rightDetected) {
        turnLeft();
    }

    // Right sensor detects line
    else if (!leftDetected && rightDetected) {
        turnRight();
    }

    // Both sensors lost the line
    else {
        stopMotors();
    }

    delay(10);
}