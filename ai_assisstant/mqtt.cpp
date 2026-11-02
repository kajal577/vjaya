#include "mqtt.h"
#include "config.h"
#include "led.h"
#include "motor.h"
#include "servo.h"

#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>

// ==================================================
// MQTT TOPICS
// ==================================================

#define MQTT_COMMAND_TOPIC "muskan/device/command"
#define MQTT_STATUS_TOPIC  "muskan/device/status"

// ==================================================
// MQTT OBJECTS
// ==================================================

WiFiClientSecure mqttSecureClient;
PubSubClient mqttClient(mqttSecureClient);

// ==================================================
// MQTT STATUS
// ==================================================

void publishMQTTStatus(const String &message)
{
    if (!mqttClient.connected())
        return;

    mqttClient.publish(
        MQTT_STATUS_TOPIC,
        message.c_str(),
        true
    );

    Serial.print("MQTT STATUS: ");
    Serial.println(message);
}

// ==================================================
// MQTT COMMAND
// ==================================================

void mqttCallback(char* topic, byte* payload, unsigned int length)
{
    String command = "";

    for (unsigned int i = 0; i < length; i++)
    {
        command += (char)payload[i];
    }

    command.trim();
    command.toUpperCase();

    Serial.println();
    Serial.println("==============================");
    Serial.println("MQTT COMMAND");
    Serial.println("==============================");
    Serial.print("Command: ");
    Serial.println(command);
    Serial.println("==============================");

    // ==================================================
    // LED
    // ==================================================

    if (command == "LED ON")
    {
        ledOn();

        Serial.println("REMOTE LED ON");

        publishMQTTStatus("LED ON");
    }

    else if (command == "LED OFF")
    {
        ledOff();

        Serial.println("REMOTE LED OFF");

        publishMQTTStatus("LED OFF");
    }

    // ==================================================
    // FAN 1
    // ==================================================

    else if (command == "FAN1 ON")
    {
        turnFan1On();

        Serial.println("REMOTE FAN 1 ON");

        publishMQTTStatus("FAN1 ON");
    }

    else if (command == "FAN1 OFF")
    {
        turnFan1Off();

        Serial.println("REMOTE FAN 1 OFF");

        publishMQTTStatus("FAN1 OFF");
    }

    // ==================================================
    // FAN 2
    // ==================================================

    else if (command == "FAN2 ON")
    {
        turnFan2On();

        Serial.println("REMOTE FAN 2 ON");

        publishMQTTStatus("FAN2 ON");
    }

    else if (command == "FAN2 OFF")
    {
        turnFan2Off();

        Serial.println("REMOTE FAN 2 OFF");

        publishMQTTStatus("FAN2 OFF");
    }

    // ==================================================
    // BOTH FANS
    // ==================================================

    else if (command == "FAN ON")
    {
        turnBothFansOn();

        Serial.println("REMOTE BOTH FANS ON");

        publishMQTTStatus("FAN ON");
    }

    else if (command == "FAN OFF")
    {
        turnBothFansOff();

        Serial.println("REMOTE BOTH FANS OFF");

        publishMQTTStatus("FAN OFF");
    }

    // ==================================================
    // GATE
    // ==================================================

    else if (command == "GATE OPEN")
    {
        gateOpen();

        Serial.println("REMOTE GATE OPEN");

        publishMQTTStatus("GATE OPEN");
    }

    else if (command == "GATE CLOSE")
    {
        gateClose();

        Serial.println("REMOTE GATE CLOSE");

        publishMQTTStatus("GATE CLOSE");
    }

    // ==================================================
    // UNKNOWN COMMAND
    // ==================================================

    else
    {
        Serial.println("Unknown MQTT command");

        publishMQTTStatus("UNKNOWN COMMAND");
    }
}

// ==================================================
// MQTT CONNECTION
// ==================================================

void reconnectMQTT()
{
    if (!WiFi.isConnected())
        return;

    while (!mqttClient.connected())
    {
        Serial.println();
        Serial.println("Connecting to MQTT...");

        String clientID = "MuskanESP32-";
        clientID += String((uint32_t)ESP.getEfuseMac(), HEX);

        if (mqttClient.connect(
                clientID.c_str(),
                MQTT_USERNAME,
                MQTT_PASSWORD))
        {
            Serial.println("MQTT CONNECTED");

            mqttClient.subscribe(MQTT_COMMAND_TOPIC);

            Serial.print("Subscribed: ");
            Serial.println(MQTT_COMMAND_TOPIC);

            publishMQTTStatus("MUSKAN ONLINE");
        }
        else
        {
            Serial.print("MQTT connection failed, state: ");
            Serial.println(mqttClient.state());

            delay(3000);
        }
    }
}

// ==================================================
// INIT MQTT
// ==================================================

void initMQTT()
{
    Serial.println();
    Serial.println("==============================");
    Serial.println("MQTT REMOTE CONTROL");
    Serial.println("==============================");

    mqttSecureClient.setInsecure();

    mqttClient.setServer(
        MQTT_HOST,
        MQTT_PORT
    );

    mqttClient.setCallback(mqttCallback);

    Serial.println("MQTT initialized");
}

// ==================================================
// HANDLE MQTT
// ==================================================

void handleMQTT()
{
    if (!WiFi.isConnected())
        return;

    if (!mqttClient.connected())
    {
        reconnectMQTT();
    }

    mqttClient.loop();
}

// ==================================================
// MQTT CONNECTION STATUS
// ==================================================

bool isMQTTConnected()
{
    return mqttClient.connected();
}