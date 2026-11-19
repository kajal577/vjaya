#include "display.h"
#include "config.h"

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

Adafruit_SSD1306 oled(
    OLED_WIDTH,
    OLED_HEIGHT,
    &Wire,
    -1
);

void initDisplay() {

    Wire.begin(OLED_SDA_PIN, OLED_SCL_PIN);

    if (!oled.begin(SSD1306_SWITCHCAPVCC, OLED_ADDRESS)) {
        Serial.println("OLED initialization failed");
        return;
    }

    oled.clearDisplay();
    oled.setTextColor(SSD1306_WHITE);
    oled.setTextSize(1);
    oled.setCursor(0, 0);

    oled.println("GPS TRACKING");
    oled.println("----------------");
    oled.println("Initializing...");
    oled.display();

    Serial.println("OLED initialized");
}

void updateDisplay(const GPSData &data) {

    oled.clearDisplay();
    oled.setTextSize(1);
    oled.setTextColor(SSD1306_WHITE);
    oled.setCursor(0, 0);

    oled.println("GPS TRACKING");
    oled.println("----------------");

    if (data.locationValid) {

        oled.print("LAT: ");
        oled.println(data.latitude, 6);

        oled.print("LON: ");
        oled.println(data.longitude, 6);

    } else {

        oled.println("Searching GPS...");
        oled.println("Waiting for fix");
    }

    if (data.altitudeValid) {
        oled.print("ALT: ");
        oled.print(data.altitude, 1);
        oled.println(" m");
    } else {
        oled.println("ALT: --");
    }

    if (data.satellitesValid) {
        oled.print("SAT: ");
        oled.println(data.satellites);
    } else {
        oled.println("SAT: --");
    }

    oled.display();
}