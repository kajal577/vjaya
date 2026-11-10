
#include "relay.h"
#include "config.h"
#include <Arduino.h>

void initRelays() {
    pinMode(LIGHT_RELAY_PIN, OUTPUT);
    pinMode(FAN_RELAY_PIN, OUTPUT);

    allAppliancesOff();
}

void lightOn() {
    digitalWrite(LIGHT_RELAY_PIN, RELAY_ON);
}

void lightOff() {
    digitalWrite(LIGHT_RELAY_PIN, RELAY_OFF);
}

void fanOn() {
    digitalWrite(FAN_RELAY_PIN, RELAY_ON);
}

void fanOff() {
    digitalWrite(FAN_RELAY_PIN, RELAY_OFF);
}

void allAppliancesOn() {
    lightOn();
    fanOn();
}

void allAppliancesOff() {
    lightOff();
    fanOff();
}
