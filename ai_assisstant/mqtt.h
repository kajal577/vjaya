#ifndef MQTT_H
#define MQTT_H

#include <Arduino.h>

void initMQTT();
void handleMQTT();

bool isMQTTConnected();

#endif