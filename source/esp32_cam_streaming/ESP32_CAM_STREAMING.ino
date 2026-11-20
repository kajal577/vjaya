
#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>

#include "config.h"
#include "wifi_manager.h"
#include "camera_module.h"

WebServer server(80);

// Main webpage
const char MAIN_PAGE[] PROGMEM = R"rawliteral(
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>VJaYa Robotics - ESP32 CAM</title>
    <style>
        body {
            background: #080d19;
            color: #ffffff;
            font-family: Arial;
            text-align: center;
            padding: 20px;
        }

        h1 {
            color: #62e6c5;
        }

        img {
            width: 100%;
            max-width: 640px;
            border: 2px solid #62e6c5;
            border-radius: 12px;
        }

        .status {
            color: #62e6c5;
            margin: 15px;
        }
    </style>
</head>
<body>
    <h1>VJaYa Robotics</h1>
    <h2>ESP32-CAM Live Streaming</h2>

    <p class="status">Camera is connected</p>

    <img src="/capture" id="camera">

    <script>
        const camera = document.getElementById("camera");

        function refreshCamera() {
            camera.src = "/capture?t=" + Date.now();
        }

        camera.onerror = function() {
            setTimeout(refreshCamera, 1000);
        };

        camera.onload = function() {
            setTimeout(refreshCamera, 100);
        };
    </script>
</body>
</html>
)rawliteral";

// Capture image
void handleCapture() {

    camera_fb_t *fb = esp_camera_fb_get();

    if (!fb) {
        server.send(500, "text/plain", "Camera capture failed");
        return;
    }

    server.setContentLength(fb->len);
    server.send(200, "image/jpeg", "");

    WiFiClient client = server.client();

    client.write(fb->buf, fb->len);

    esp_camera_fb_return(fb);
}

// Homepage
void handleRoot() {
    server.send_P(200, "text/html", MAIN_PAGE);
}

// Start web server
void startWebServer() {

    server.on("/", HTTP_GET, handleRoot);

    server.on("/capture", HTTP_GET, handleCapture);

    server.begin();

    Serial.println("Web server started!");
}

void setup() {

    Serial.begin(115200);

    Serial.println();
    Serial.println("================================");
    Serial.println("VJaYa Robotics");
    Serial.println("ESP32-CAM Live Video Streaming");
    Serial.println("================================");

    if (!initCamera()) {
        Serial.println("Camera failed. Restarting...");
        delay(3000);
        ESP.restart();
    }

    if (!connectWiFi()) {
        Serial.println("WiFi failed. Restarting...");
        delay(3000);
        ESP.restart();
    }

    startWebServer();

    Serial.println();
    Serial.println("Open this address in your browser:");
    Serial.println(WiFi.localIP());
}

void loop() {

    server.handleClient();

}
