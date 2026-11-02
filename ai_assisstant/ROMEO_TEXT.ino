//
#include "config.h"

#include "wifi_manager.h"
#include "display.h"
#include "server.h"
#include "robot_face.h"
#include "led.h"
#include "motor.h"
#include "servo.h"
#include "mqtt.h"

#include <DFRobotDFPlayerMini.h>

// ==================================================
// DFPLAYER
// ==================================================

DFRobotDFPlayerMini myDFPlayer;

// ==================================================
// SETUP
// ==================================================

void setup()
{
    Serial.begin(115200);
    delay(1000);

    Serial.println();
    Serial.println("==============================");
    Serial.println("ESP32 AI TEXT ASSISTANT");
    Serial.println("==============================");

    // ------------------------------------------------
    // OLED
    // ------------------------------------------------

    initDisplay();

    displayStatus(
        "MUSKAN",
        "AI ASSISTANT",
        "Starting..."
    );

    // ------------------------------------------------
    // LED
    // ------------------------------------------------

    initLED();

    // ------------------------------------------------
    // MOTORS
    // ------------------------------------------------

    initMotors();


    // ------------------------------------------------
    // FAN RELAY
    // ------------------------------------------------

   initServo();

    Serial.println();
    Serial.println("==============================");
    Serial.println("FAN RELAY SYSTEM READY");
    Serial.print("Relay Pin: GPIO ");
   // Serial.println(FAN_RELAY_PIN);
    Serial.println("==============================");

    // ------------------------------------------------
    // WIFI
    // ------------------------------------------------

    displayStatus(
        "Connecting",
        "to WiFi...",
        ""
    );

    Serial.println();
    Serial.println("Connecting to WiFi...");

    connectWiFi();

    

    // ------------------------------------------------
    // MQTT
    // ------------------------------------------------

    initMQTT();

    // ------------------------------------------------
    // WEB SERVER
    // ------------------------------------------------

    initServer();

    Serial.println();
    Serial.println("==============================");
    Serial.println("MUSKAN READY");
    Serial.println("==============================");

    
    // ------------------------------------------------
    // OLED READY
    // ------------------------------------------------

    displayStatus(
        "MUSKAN READY",
        "REMOTE CONTROL",
        "ONLINE"
    );

    delay(2000);

    showRobotFace();
}

// ==================================================
// LOOP
// ==================================================

void loop()
{
    // ------------------------------------------------
    // LOCAL WEB SERVER
    // ------------------------------------------------

    handleServer();

    // ------------------------------------------------
    // MQTT REMOTE CONTROL
    // ------------------------------------------------

    handleMQTT();
}
//