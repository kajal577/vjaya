#include "groq_client.h"
#include "config.h"
#include "wifi_manager.h"
#include "led.h"
#include "motor.h"
#include "display.h"

#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <DFRobotDFPlayerMini.h>

extern DFRobotDFPlayerMini myDFPlayer;


// =====================================================
// CONVERSATION MEMORY
// =====================================================

#define MAX_HISTORY 6

struct ChatMessage
{
    String role;
    String content;
};

ChatMessage chatHistory[MAX_HISTORY];

int historyCount = 0;


// =====================================================
// LOCAL COMMAND PROCESSING
// =====================================================

bool processLocalCommand(const String &question, String &answer)
{
    String command = question;

    command.toLowerCase();
    command.trim();

    // Remove common punctuation
    command.replace(".", "");
    command.replace(",", "");
    command.replace("!", "");
    command.replace("?", "");


    // =================================================
    // LED ON
    // =================================================

    if (
        command == "led on" ||
        command.indexOf("turn on led") >= 0 ||
        command.indexOf("turn on the led") >= 0 ||
        command.indexOf("turn the led on") >= 0 ||
        command.indexOf("switch on led") >= 0 ||
        command.indexOf("switch on the led") >= 0 ||
        command.indexOf("switch the led on") >= 0
    )
    {
        Serial.println("==============================");
        Serial.println("LOCAL COMMAND");
        Serial.println("Command: LED ON");
        Serial.println("==============================");

        ledOn();

        answer = "LED is now ON.";
        return true;
    }


    // =================================================
    // LED OFF
    // =================================================

    if (
        command == "led off" ||
        command.indexOf("turn off led") >= 0 ||
        command.indexOf("turn off the led") >= 0 ||
        command.indexOf("turn the led off") >= 0 ||
        command.indexOf("switch off led") >= 0 ||
        command.indexOf("switch off the led") >= 0 ||
        command.indexOf("switch the led off") >= 0
    )
    {
        Serial.println("==============================");
        Serial.println("LOCAL COMMAND");
        Serial.println("Command: LED OFF");
        Serial.println("==============================");

        ledOff();

        answer = "LED is now OFF.";
        return true;
    }

// =================================================
// FAN 1 ON
// =================================================

if (
    command == "fan 1 on" ||
    command == "fan one on" ||
    command.indexOf("fan 1 on") >= 0
)
{
    Serial.println("==============================");
    Serial.println("LOCAL COMMAND");
    Serial.println("Command: FAN 1 ON");
    Serial.println("==============================");

    turnFanOn();

    answer = "Fan 1 is now ON.";
    return true;
}


// =================================================
// FAN 1 OFF
// =================================================

if (
    command == "fan 1 off" ||
    command == "fan one off" ||
    command.indexOf("fan 1 off") >= 0
)
{
    Serial.println("==============================");
    Serial.println("LOCAL COMMAND");
    Serial.println("Command: FAN 1 OFF");
    Serial.println("==============================");

    turnFanOff();

    answer = "Fan 1 is now OFF.";
    return true;
}


// =================================================
// FAN 2 ON
// =================================================

if (
    command == "fan 2 on" ||
    command == "fan two on" ||
    command.indexOf("fan 2 on") >= 0
)
{
    Serial.println("==============================");
    Serial.println("LOCAL COMMAND");
    Serial.println("Command: FAN 2 ON");
    Serial.println("==============================");

    turnFan2On();

    answer = "Fan 2 is now ON.";
    return true;
}


// =================================================
// FAN 2 OFF
// =================================================

if (
    command == "fan 2 off" ||
    command == "fan two off" ||
    command.indexOf("fan 2 off") >= 0
)
{
    Serial.println("==============================");
    Serial.println("LOCAL COMMAND");
    Serial.println("Command: FAN 2 OFF");
    Serial.println("==============================");

    turnFan2Off();

    answer = "Fan 2 is now OFF.";
    return true;
}
    


    // =================================================
    // MUSIC OFF
    // =================================================

    if (
        command == "music off" ||
        command == "stop music" ||
        command == "turn off music" ||
        command.indexOf("music off") >= 0 ||
        command.indexOf("stop music") >= 0 ||
        command.indexOf("turn off music") >= 0
    )
    {
        Serial.println("==============================");
        Serial.println("LOCAL COMMAND");
        Serial.println("Command: MUSIC OFF");
        Serial.println("==============================");

        myDFPlayer.stop();

        answer = "Music turned off.";
        return true;
    }


    // =================================================
    // MUSIC ON
    // =================================================

    if (
        command == "music on" ||
        command == "play music" ||
        command == "start music" ||
        command.indexOf("music on") >= 0 ||
        command.indexOf("play music") >= 0 ||
        command.indexOf("start music") >= 0
    )
    {
        Serial.println("==============================");
        Serial.println("LOCAL COMMAND");
        Serial.println("Command: MUSIC ON");
        Serial.println("==============================");

        myDFPlayer.play(1);

        answer = "Playing music.";
        return true;
    }


    // No local command found
    return false;
}


// =====================================================
// CLEAR OLD MEMORY
// =====================================================

void clearConversation()
{
    for (int i = 0; i < MAX_HISTORY; i++)
    {
        chatHistory[i].role = "";
        chatHistory[i].content = "";
    }

    historyCount = 0;

    Serial.println("Conversation memory cleared");
}


// =====================================================
// ADD MESSAGE TO MEMORY
// =====================================================

void addToHistory(const String &role, const String &content)
{
    if (historyCount >= MAX_HISTORY)
    {
        for (int i = 0; i < MAX_HISTORY - 1; i++)
        {
            chatHistory[i] = chatHistory[i + 1];
        }

        historyCount = MAX_HISTORY - 1;
    }

    chatHistory[historyCount].role = role;
    chatHistory[historyCount].content = content;

    historyCount++;
}


// =====================================================
// ASK GROQ
// =====================================================

String askGroq(const String &question)
{
    Serial.println();
    Serial.println("==============================");
    Serial.println("GROQ REQUEST");
    Serial.println("==============================");


    // =================================================
    // CHECK LOCAL COMMAND FIRST
    // =================================================

    String localAnswer;

    if (processLocalCommand(question, localAnswer))
    {
        Serial.println("Local command handled.");
        Serial.println("Groq request skipped.");

        Serial.println();
        Serial.println("AI:");
        Serial.println(localAnswer);
        Serial.println();


        displayText(localAnswer);
        return localAnswer;
    }


    // =================================================
    // NORMAL GROQ REQUEST
    // =================================================

    if (!isWiFiConnected())
    {
        Serial.println("❌ WiFi not connected");
        return "WiFi not connected";
    }


    // =================================================
    // HTTPS CONNECTION
    // =================================================

    WiFiClientSecure client;
    client.setInsecure();

    HTTPClient https;


    if (!https.begin(client, GROQ_URL))
    {
        Serial.println("❌ HTTPS connection failed");
        return "Connection failed";
    }


    // =================================================
    // HTTP HEADERS
    // =================================================

    https.addHeader("Content-Type", "application/json");
    https.addHeader(
        "Authorization",
        "Bearer " + String(GROQ_API_KEY)
    );


    // =================================================
    // BUILD JSON REQUEST
    // =================================================

    JsonDocument docRequest;

    // IMPORTANT:
    // Use the model defined in config.h.
    // Do NOT hard-code the old llama model here.
    docRequest["model"] = GROQ_MODEL;

    JsonArray messages = docRequest["messages"].to<JsonArray>();


    // System personality
    JsonObject systemMessage = messages.add<JsonObject>();

    systemMessage["role"] = "system";

    systemMessage["content"] =
        "Your name is Muskan. "
        "You are a friendly AI assistant running on an ESP32. "
        "Answer naturally like a human. "
        "Keep answers concise and easy to understand. "
        "Do not use markdown tables. "
        "Do not use unnecessary formatting.";


    // Previous conversation
    for (int i = 0; i < historyCount; i++)
    {
        JsonObject historyMessage = messages.add<JsonObject>();

        historyMessage["role"] = chatHistory[i].role;
        historyMessage["content"] = chatHistory[i].content;
    }


    // Current user question
    JsonObject userMessage = messages.add<JsonObject>();

    userMessage["role"] = "user";
    userMessage["content"] = question;


    // Serialize JSON
    String jsonPayload;

    serializeJson(docRequest, jsonPayload);


    // =================================================
    // SERIAL DEBUG
    // =================================================

    Serial.println("➔ Sending cloud request to Groq API...");

    Serial.print("Groq URL: ");
    Serial.println(GROQ_URL);

    Serial.print("Groq Model: ");
    Serial.println(GROQ_MODEL);


    // =================================================
    // SEND REQUEST
    // =================================================

    int httpCode = https.POST(jsonPayload);


    // =================================================
    // READ SERVER RESPONSE
    // =================================================

    String responseStr = https.getString();


    Serial.print("HTTP Code: ");
    Serial.println(httpCode);


    // =================================================
    // SUCCESS
    // =================================================

    if (httpCode == HTTP_CODE_OK || httpCode == 200)
    {
        JsonDocument docResponse;

        DeserializationError error =
            deserializeJson(docResponse, responseStr);


        if (!error)
        {
            //aiReply:
            String aiReply =
                docResponse["choices"][0]["message"]["content"].as<String>();


            // Save conversation
            addToHistory("user", question);
            addToHistory("assistant", aiReply);


            Serial.println();
            Serial.println("AI:");
            Serial.println(aiReply);
            Serial.println("==============================");


            https.end();
            displayText(aiReply);

            return aiReply;
        }
        else
        {
            Serial.println("❌ JSON parsing failed");

            Serial.println("Groq response:");
            Serial.println(responseStr);


            https.end();

            return "AI response could not be read.";
        }
    }


    // =================================================
    // ERROR
    // =================================================

    Serial.print("❌ HTTP Error Code: ");
    Serial.println(httpCode);

    Serial.println("Groq Server Response:");
    Serial.println(responseStr);

    Serial.println("==============================");


    String errorMessage =
        "Error: Groq HTTP " + String(httpCode);


    https.end();

    return errorMessage;
}