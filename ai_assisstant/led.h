#ifndef LED_H
#define LED_H

#include <Arduino.h>

#define LED_PIN 18

void initLED();
void ledOn();
void ledOff();
void toggleLED();
bool isLEDOn();

#endif