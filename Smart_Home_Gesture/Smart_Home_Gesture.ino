
#include "config.h"
#include "relay.h"
#include "bluetooth.h"

void setup() {

    Serial.begin(9600);

    initRelays();
    initBluetooth();

    Serial.println("SMART HOME GESTURE AUTOMATION");
    Serial.println("Bluetooth Ready");
}

void loop() {

    processBluetooth();

}
