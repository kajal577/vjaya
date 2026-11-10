
#include "motor.h"
#include "bluetooth.h"

void setup() {
    Serial.begin(9600);

    initMotors();
    initBluetooth();

    Serial.println("Bluetooth Robot Car Ready");
}

void loop() {
    processBluetooth();
}
