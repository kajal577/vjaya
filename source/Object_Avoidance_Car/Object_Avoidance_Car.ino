#include "config.h"
#include "motor.h"
#include "ultrasonic.h"
#include "scanner.h"

void setup() {
    Serial.begin(9600);

    initMotors();
    initUltrasonic();
    initScanner();

    Serial.println("Object Avoidance Car Started");

    delay(1000);
}

void loop() {
    int frontDistance = scanFront();

    Serial.print("Front Distance: ");
    Serial.println(frontDistance);

    if (frontDistance > OBSTACLE_DISTANCE) {
        moveForward();
    }
    else {
        stopMotors();
        delay(200);

        moveBackward();
        delay(MOTOR_REVERSE_TIME);

        stopMotors();
        delay(200);

        int leftDistance = scanLeft();
        int rightDistance = scanRight();

        Serial.print("Left: ");
        Serial.println(leftDistance);

        Serial.print("Right: ");
        Serial.println(rightDistance);

        if (leftDistance > rightDistance &&
            leftDistance > SAFE_DISTANCE) {

            turnLeft();
            delay(MOTOR_TURN_TIME);
        }
        else if (rightDistance > SAFE_DISTANCE) {

            turnRight();
            delay(MOTOR_TURN_TIME);
        }
        else {
            moveBackward();
            delay(500);
        }

        stopMotors();
        delay(100);
    }

    delay(50);
}