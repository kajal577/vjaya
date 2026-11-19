#ifndef CONFIG_H
#define CONFIG_H

#include <Arduino.h>

// GPS NEO-6M connections
#define GPS_RX_PIN 16
#define GPS_TX_PIN 17
#define GPS_BAUD_RATE 9600

// OLED SSD1306 I2C connections
#define OLED_SDA_PIN 21
#define OLED_SCL_PIN 22
#define OLED_ADDRESS 0x3C

// OLED dimensions
#define OLED_WIDTH 128
#define OLED_HEIGHT 64

// Serial Monitor
#define SERIAL_BAUD_RATE 115200

// Display refresh interval
#define DISPLAY_UPDATE_INTERVAL 1000

#endif