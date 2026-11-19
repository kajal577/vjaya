
#include "walking.h"
#include "servo_control.h"
#include "balance.h"
#include "config.h"

static bool walking = false;

// Initial experimental gait poses.
// Adjust only after checking servo directions and linkages.

static void applyPose(
    int leftRoll,
    int leftHip,
    int leftKnee,
    int rightRoll,
    int rightHip,
    int rightKnee
) {
    setServoAngle(LEFT_HIP_ROLL, leftRoll);
    setServoAngle(LEFT_HIP_PITCH, leftHip);
    setServoAngle(LEFT_KNEE, leftKnee);

    setServoAngle(RIGHT_HIP_ROLL, rightRoll);
    setServoAngle(RIGHT_HIP_PITCH, rightHip);
    setServoAngle(RIGHT_KNEE, rightKnee);
}

void stopWalking() {

    walking = false;
    standPosition();

    Serial.println("Walking stopped");
}

void walkForward() {

    walking = true;

    Serial.println("Forward gait requested");

    while (walking) {

        // Left leg swing phase
        applyPose(95, 105, 65, 85, 90, 90);
        delay(WALK_STEP_TIME / 2);

        // Right leg swing phase
        applyPose(85, 90, 90, 95, 105, 65);
        delay(WALK_STEP_TIME / 2);

        // Serial command can interrupt movement
        if (Serial.available()) {
            char command = Serial.read();

            if (command == 'S' || command == 's') {
                stopWalking();
            }
        }
    }
}

void walkBackward() {

    Serial.println("Backward gait requested");

    applyPose(95, 75, 110, 85, 90, 90);
    delay(WALK_STEP_TIME / 2);

    applyPose(85, 90, 90, 95, 75, 110);
    delay(WALK_STEP_TIME / 2);

    standPosition();
}

void turnLeft() {

    Serial.println("Left turn requested");

    applyPose(100, 105, 75, 90, 90, 90);
    delay(WALK_STEP_TIME);

    standPosition();
}

void turnRight() {

    Serial.println("Right turn requested");

    applyPose(90, 90, 90, 100, 105, 75);
    delay(WALK_STEP_TIME);

    standPosition();
}
