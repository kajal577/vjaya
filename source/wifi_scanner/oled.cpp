//
#include "oled.h"

#include <Wire.h>
#include <WiFi.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// =====================================================
// OLED CONFIGURATION
// =====================================================

#define OLED_WIDTH   128
#define OLED_HEIGHT   64
#define OLED_ADDRESS 0x3C

#define OLED_SDA 4
#define OLED_SCL 15

Adafruit_SSD1306 display(
  OLED_WIDTH,
  OLED_HEIGHT,
  &Wire,
  -1
);

// =====================================================
// INITIALIZE OLED
// =====================================================

void initOLED()
{
  Wire.begin(
    OLED_SDA,
    OLED_SCL
  );

  if (!display.begin(
        SSD1306_SWITCHCAPVCC,
        OLED_ADDRESS
      ))
  {
    Serial.println("OLED FAILED");
    return;
  }

  display.clearDisplay();

  display.setTextColor(
    SSD1306_WHITE
  );

  display.setTextSize(1);

  display.setCursor(0, 0);

  display.println("MUSKAN WIFI");
  display.println("----------------");
  display.println("OLED READY");

  display.display();

  Serial.println("OLED initialized");
}

// =====================================================
// CLEAR OLED
// =====================================================

void oledClear()
{
  display.clearDisplay();
  display.display();
}

// =====================================================
// DISPLAY TEXT
// =====================================================

void oledShow(
  const String &line1,
  const String &line2,
  const String &line3,
  const String &line4,
  const String &line5,
  const String &line6,
  const String &line7,
  const String &line8
)
{
  display.clearDisplay();

  display.setTextColor(
    SSD1306_WHITE
  );

  display.setTextSize(1);

  display.setCursor(0, 0);

  display.println(line1);
  display.println(line2);
  display.println(line3);
  display.println(line4);
  display.println(line5);
  display.println(line6);
  display.println(line7);
  display.println(line8);

  display.display();
}

// =====================================================
// DISPLAY WIFI NETWORK LIST
// =====================================================

void oledShowWiFiList(int networkCount)
{
  display.clearDisplay();

  display.setTextColor(
    SSD1306_WHITE
  );

  display.setTextSize(1);

  // Header
  display.setCursor(0, 0);
  display.println("WIFI SCANNER");
  display.println("----------------");

  // No networks
  if (networkCount <= 0)
  {
    display.println("No WiFi found");
    display.display();

    Serial.println("No WiFi networks found");

    return;
  }

  // Show maximum 6 networks
  int maxDisplay = min(networkCount, 6);

  for (int i = 0; i < maxDisplay; i++)
  {
    String ssid = WiFi.SSID(i);

    // Hidden network
    if (ssid.length() == 0)
    {
      ssid = "Hidden";
    }

    // OLED width limitation
    if (ssid.length() > 13)
    {
      ssid = ssid.substring(0, 13);
    }

    int rssi = WiFi.RSSI(i);

    display.setCursor(
      0,
      16 + (i * 8)
    );

    // Network number
    display.print(i + 1);
    display.print(" ");

    // SSID
    display.print(ssid);

    // Signal
    display.setCursor(
      95,
      16 + (i * 8)
    );

    display.print(rssi);
  }

  display.display();

  Serial.println();
  Serial.println("==============================");
  Serial.println("OLED WIFI LIST");
  Serial.println("==============================");

  for (int i = 0; i < networkCount; i++)
  {
    Serial.print(i + 1);
    Serial.print(". ");
    Serial.print(WiFi.SSID(i));
    Serial.print("  ");
    Serial.print(WiFi.RSSI(i));
    Serial.println(" dBm");
  }
}
