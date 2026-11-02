#ifndef CONFIG_H
#define CONFIG_H

// ==============================
// WiFi Configuration
// ==============================

#define WIFI_SSID "Sadhana@JIO5G"
#define WIFI_PASSWORD "Sadhana@9204"


// ==============================
// Groq API Configuration
// ==============================

#define GROQ_API_KEY "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"

#define GROQ_URL \
  "https://api.groq.com/openai/v1/chat/completions"

//#define GROQ_MODEL "llama-3.1-8b-instant"
//#define GROQ_MODEL "llama-3.1-8b-instant"
#define GROQ_MODEL "openai/gpt-oss-20b"

// ==============================
// MQTT REMOTE CONTROL
// ==============================

#define MQTT_HOST "brightmason-65c25e58.a02.usw2.aws.hivemq.cloud"
#define MQTT_PORT 8883
#define MQTT_USERNAME "vijayyadav@420"
#define MQTT_PASSWORD "SanjuMuskan@420"

// ==============================
// OLED Configuration
// ==============================

#define OLED_SDA 4
#define OLED_SCL 15

#define OLED_WIDTH 128
#define OLED_HEIGHT 64

#define OLED_ADDRESS 0x3C
#define OLED_RESET -1


// LED CONFIGURATION

//GPIOPIN = 18

// ==============================
// Web Server
// ==============================

#define SERVER_PORT 80

#endif