#ifndef WIFI_MANAGER_H
#define WIFI_MANAGER_H

#include <Arduino.h>

void connectWiFi();
bool isWiFiConnected();
String getIPAddress();

#endif