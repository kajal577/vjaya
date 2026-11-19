
#ifndef JOYSTICK_H
#define JOYSTICK_H

#include <Arduino.h>

void initJoystick();

void readJoystick();

int getJoystickX1();
int getJoystickY1();

int getJoystickX2();
int getJoystickY2();

bool isGripperButtonPressed();

#endif