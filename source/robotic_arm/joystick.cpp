
#include "joystick.h"
#include "config.h"

// Store joystick readings
static int joyX1 = JOYSTICK_CENTER;
static int joyY1 = JOYSTICK_CENTER;

static int joyX2 = JOYSTICK_CENTER;
static int joyY2 = JOYSTICK_CENTER;

void initJoystick() {

    pinMode(JOY1_X_PIN, INPUT);
    pinMode(JOY1_Y_PIN, INPUT);

    pinMode(JOY2_X_PIN, INPUT);
    pinMode(JOY2_Y_PIN, INPUT);

    pinMode(JOY2_SW_PIN, INPUT_PULLUP);
}

void readJoystick() {

    joyX1 = analogRead(JOY1_X_PIN);
    joyY1 = analogRead(JOY1_Y_PIN);

    joyX2 = analogRead(JOY2_X_PIN);
    joyY2 = analogRead(JOY2_Y_PIN);
}

int getJoystickX1() {
    return joyX1;
}

int getJoystickY1() {
    return joyY1;
}

int getJoystickX2() {
    return joyX2;
}

int getJoystickY2() {
    return joyY2;
}

bool isGripperButtonPressed() {

    return digitalRead(JOY2_SW_PIN) == LOW;
}