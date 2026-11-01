
#ifndef OLED_H
#define OLED_H

#include <Arduino.h>

void initOLED();

void oledClear();

void oledShow(
  const String &line1,
  const String &line2 = "",
  const String &line3 = "",
  const String &line4 = "",
  const String &line5 = "",
  const String &line6 = "",
  const String &line7 = "",
  const String &line8 = ""
);

// Display scanned Wi-Fi networks
void oledShowWiFiList(int networkCount);

#endif
