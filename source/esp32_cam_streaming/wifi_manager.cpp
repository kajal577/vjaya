
#include "wifi_manager.h"
#include "config.h"
#include <WiFi.h>

bool connectWiFi() {

    WiFi.mode(WIFI_STA);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

    Serial.print("Connecting to WiFi");

    unsigned long startTime = millis();

    while (WiFi.status() != WL_CONNECTED &&
           millis() - startTime < 20000) {

        delay(500);
        Serial.print(".");
    }

    if (WiFi.status() == WL_CONNECTED) {

        Serial.println();
        Serial.println("WiFi Connected!");
        Serial.print("IP Address: ");
        Serial.println(WiFi.localIP());

        return true;
    }

    Serial.println();
    Serial.println("WiFi Connection Failed!");

    return false;
}

String getWiFiIP() {

    if (WiFi.status() == WL_CONNECTED) {
        return WiFi.localIP().toString();
    }

    return "Not Connected";
}
