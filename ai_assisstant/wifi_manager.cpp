#include "wifi_manager.h"
#include "config.h"

#include <WiFi.h>

void connectWiFi()
{
    Serial.println();
    Serial.println("Connecting to WiFi...");
    Serial.println(WIFI_SSID);

    WiFi.mode(WIFI_STA);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

    unsigned long startTime = millis();

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");

        if (millis() - startTime > 20000)
        {
            Serial.println();
            Serial.println("WiFi connection timeout");
            return;
        }
    }

    Serial.println();
    Serial.println("WiFi connected");

    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
}


bool isWiFiConnected()
{
    return WiFi.status() == WL_CONNECTED;
}


String getIPAddress()
{
    if (!isWiFiConnected())
    {
        return "0.0.0.0";
    }

    return WiFi.localIP().toString();
}