#include "led.h"

bool ledState = false;

void initLED()
{
    pinMode(LED_PIN, OUTPUT);

    digitalWrite(LED_PIN, LOW);

    ledState = false;

    Serial.println("LED initialized");
    Serial.println("LED GPIO : 18");
    Serial.println("LED State: OFF");
}

void ledOn()
{
    digitalWrite(LED_PIN, HIGH);
    ledState = true;

    Serial.println("LED ON");
}

void ledOff()
{
    digitalWrite(LED_PIN, LOW);
    ledState = false;

    Serial.println("LED OFF");
}

void toggleLED()
{
    if (ledState)
    {
        ledOff();
    }
    else
    {
        ledOn();
    }
}

bool isLEDOn()
{
    return ledState;
}