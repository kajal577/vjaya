
#include "servo_control.h"
#include "joystick.h"
#include "config.h"

#include <Servo.h>

static Servo armServos[TOTAL_SERVOS];

static int servoAngles[TOTAL_SERVOS] = {
    90,  // Base
    90,  // Shoulder
    90,  // Elbow
    90,  // Wrist
    GRIPPER_OPEN_ANGLE
};

static bool gripperClosed = false;

static bool previousButtonState = HIGH;

static void moveServo(uint8_t index, int direction) {

    if (index >= TOTAL_SERVOS || direction == 0) {
        return;
    }

    servoAngles[index] += direction * SERVO_STEP;

    servoAngles[index] = constrain(
        servoAngles[index],
        SERVO_MIN_ANGLE[index],
        SERVO_MAX_ANGLE[index]
    );

    armServos[index].write(servoAngles[index]);
}

static int joystickDirection(int value) {

    if (value > JOYSTICK_CENTER + JOYSTICK_DEADZONE) {
        return 1;
    }

    if (value < JOYSTICK_CENTER - JOYSTICK_DEADZONE) {
        return -1;
    }

    return 0;
}

void initServoControl() {

    for (uint8_t i = 0; i < TOTAL_SERVOS; i++) {

        armServos[i].attach(SERVO_PINS[i]);

        servoAngles[i] = constrain(
            servoAngles[i],
            SERVO_MIN_ANGLE[i],
            SERVO_MAX_ANGLE[i]
        );

        armServos[i].write(servoAngles[i]);
    }

    delay(500);
}

void updateServoControl() {

    // Joystick 1 controls base and shoulder
    moveServo(0, joystickDirection(getJoystickX1()));
    moveServo(1, joystickDirection(getJoystickY1()));

    // Joystick 2 controls elbow and wrist
    moveServo(2, joystickDirection(getJoystickX2()));
    moveServo(3, joystickDirection(getJoystickY2()));

    // Gripper button toggles open / closed
    bool currentButtonState = isGripperButtonPressed();

    if (previousButtonState == HIGH &&
        currentButtonState == LOW) {

        gripperClosed = !gripperClosed;

        if (gripperClosed) {
            servoAngles[4] = GRIPPER_CLOSE_ANGLE;
        } else {
            servoAngles[4] = GRIPPER_OPEN_ANGLE;
        }

        armServos[4].write(servoAngles[4]);
    }

    previousButtonState = currentButtonState;
}