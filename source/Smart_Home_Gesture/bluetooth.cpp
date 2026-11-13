
#include "bluetooth.h"
#include "config.h"
#include "relay.h"

#include <Arduino.h>
#include <SoftwareSerial.h>

SoftwareSerial bluetooth(BT_RX_PIN, BT_TX_PIN);

void initBluetooth() {
    bluetooth.begin(BT_BAUD_RATE);
}

void processBluetooth() {

    if (!bluetooth.available()) {
        return;
    }

    char command = bluetooth.read();

    switch (command) {

        case '1':
            lightOn();
            break;

        case '2':
            lightOff();
            break;

        case '3':
            fanOn();
            break;

        case '4':
            fanOff();
            break;

        case '5':
            allAppliancesOn();
            break;

        case '0':
            allAppliancesOff();
            break;
    }
}
