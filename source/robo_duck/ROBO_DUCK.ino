
#include "config.h"
#include "servo_control.h"
#include "walking.h"
#include "balance.h"

void setup() {

    Serial.begin(115200);

    delay(1000);

    Serial.println();
    Serial.println("======================");
    Serial.println("     ROBO DUCK");
    Serial.println("======================");

    initServos();

    delay(500);

    standPosition();

    Serial.println("ROBO DUCK READY");

    Serial.println("Commands:");
    Serial.println("F - Forward");
    Serial.println("B - Backward");
    Serial.println("L - Turn Left");
    Serial.println("R - Turn Right");
    Serial.println("S - Stop");
    Serial.println("H - Home Position");
}

void loop() {

    if (Serial.available()) {

        char command = Serial.read();

        switch (command) {

            case 'F':
            case 'f':
                walkForward();
                break;

            case 'B':
            case 'b':
                walkBackward();
                break;

            case 'L':
            case 'l':
                turnLeft();
                break;

            case 'R':
            case 'r':
                turnRight();
                break;

            case 'S':
            case 's':
                stopWalking();
                break;

            case 'H':
            case 'h':
                standPosition();
                Serial.println("Home position");
                break;

            default:
                break;
        }
    }
}
