#pragma once
#include <Arduino.h>
#include <SoftwareSerial.h>

void initBluetooth();
void readBluetooth();
char getMovementCommand();
bool isArmed();