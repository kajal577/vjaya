#ifndef DISPLAY_H
#define DISPLAY_H

#include <Arduino.h>

void initDisplay();

void clearDisplay();

void displayStatus(
    const String &line1,
    const String &line2 = "",
    const String &line3 = ""
);

void displayText(
    const String &text
);

#endif