#include <WiFi.h>
#include <WebServer.h>
#include <ESP32Servo.h>
#include <WiFiClientSecure.h>
#include <HTTPClient.h>

// ==========================================
// 🌐 NETWORK & TELEGRAM CONFIGURATION
// ==========================================

const char* ssid     = "Sadhana@JIO5G";
const char* password = "Sadhana@9204";

// IMPORTANT:
// Replace these with your NEW Telegram bot credentials.
const String botToken = "8910648390:AAFRkv6ZHZyk-8zTix81hWvrXdDdHo4x4VU";
const String chatId   = "6233681139";

WebServer server(80);
Servo doorServo;

// ==========================================
// 📌 PIN DEFINITIONS
// ==========================================

const int servoPin     = 13;
const int greenLed     = 14;
const int redLed       = 12;
const int vibrationPin = 15;

// Servo positions
const int LOCKED_ANGLE   = 0;
const int UNLOCKED_ANGLE = 90;

// ==========================================
// ⏱️ SECURITY TIMING
// ==========================================

// Minimum time between Telegram alerts
const unsigned long alertCooldown = 30000;

// Prevent repeated triggering from one vibration
const unsigned long vibrationDebounce = 1000;

unsigned long lastAlertTime = 0;
unsigned long lastVibrationTime = 0;

// ==========================================
// 📲 URL ENCODING
// ==========================================

String urlEncode(String str)
{
  String encodedString = "";

  char c;
  char code0;
  char code1;

  for (int i = 0; i < str.length(); i++)
  {
    c = str.charAt(i);

    if (isalnum(c))
    {
      encodedString += c;
    }
    else if (c == ' ')
    {
      encodedString += '+';
    }
    else
    {
      code1 = (c & 0x0F) + '0';

      if ((c & 0x0F) > 9)
      {
        code1 = (c & 0x0F) - 10 + 'A';
      }

      c = (c >> 4) & 0x0F;

      code0 = c + '0';

      if (c > 9)
      {
        code0 = c - 10 + 'A';
      }

      encodedString += '%';
      encodedString += code0;
      encodedString += code1;
    }
  }

  return encodedString;
}

// ==========================================
// 📲 TELEGRAM ALERT
// ==========================================

bool sendTelegramAlert(String message)
{
  Serial.println();
  Serial.println("================================");
  Serial.println("TELEGRAM ALERT");
  Serial.println("================================");

  // Check WiFi first
  if (WiFi.status() != WL_CONNECTED)
  {
    Serial.println("❌ WiFi is not connected.");
    return false;
  }

  Serial.print("WiFi IP: ");
  Serial.println(WiFi.localIP());

  WiFiClientSecure client;

  // For testing.
  // This skips certificate verification.
  client.setInsecure();

  HTTPClient https;

  // ==========================================
  // CORRECT TELEGRAM API URL
  // ==========================================

  String url =
      "https://api.telegram.org/bot" +
      botToken +
      "/sendMessage";

  Serial.println("Telegram URL:");
  Serial.println(url);

  // Start HTTPS connection
  if (!https.begin(client, url))
  {
    Serial.println("❌ HTTPS connection could not be started.");
    return false;
  }

  https.addHeader(
      "Content-Type",
      "application/x-www-form-urlencoded"
  );

  String requestData =
      "chat_id=" +
      chatId +
      "&text=" +
      urlEncode(message);

  Serial.println("Sending Telegram message...");

  int httpCode = https.POST(requestData);

  Serial.print("HTTP Code: ");
  Serial.println(httpCode);

  // ==========================================
  // SUCCESS
  // ==========================================

  if (httpCode > 0)
  {
    String response = https.getString();

    Serial.println("Telegram response:");
    Serial.println(response);

    if (httpCode == 200)
    {
      Serial.println("✅ ALERT SENT SUCCESSFULLY!");
      https.end();
      return true;
    }
    else
    {
      Serial.println("⚠️ Telegram returned an error.");
    }
  }

  // ==========================================
  // CONNECTION ERROR
  // ==========================================

  else
  {
    Serial.print("❌ Telegram connection failed: ");
    Serial.println(https.errorToString(httpCode));
  }

  https.end();

  return false;
}

// ==========================================
// 🔐 LOCK DOOR
// ==========================================

void lockDoor()
{
  doorServo.write(LOCKED_ANGLE);

  digitalWrite(redLed, HIGH);
  digitalWrite(greenLed, LOW);

  Serial.println("➔ SECURITY ACTION: DOOR LOCKED 🔒");
}

// ==========================================
// 🔓 UNLOCK DOOR
// ==========================================

void unlockDoor()
{
  doorServo.write(UNLOCKED_ANGLE);

  digitalWrite(redLed, LOW);
  digitalWrite(greenLed, HIGH);

  Serial.println("➔ SECURITY ACTION: DOOR UNLOCKED 🔓");
}

// ==========================================
// 📄 HTML WEB PAGE
// ==========================================

const char index_html[] PROGMEM = R"rawliteral(

<!DOCTYPE html>

<html>

<head>

<meta name="viewport"
content="width=device-width, initial-scale=1">

<title>Smart Lock Console</title>

<style>

body {
  font-family: Arial, sans-serif;
  background: #121212;
  color: white;
  text-align: center;
  margin: 0;
  padding: 20px;
}

.container {
  max-width: 500px;
  margin: auto;
  padding: 20px;
  background: #1e1e1e;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.5);
}

h1 {
  color: #00adb5;
  font-size: 24px;
}

textarea {
  width: 90%;
  height: 60px;
  padding: 10px;
  font-size: 16px;
  border-radius: 8px;
  border: none;
  background: #2d2d2d;
  color: white;
  resize: none;
  margin-bottom: 15px;
}

button {
  padding: 12px 24px;
  font-size: 16px;
  font-weight: bold;
  margin: 8px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.btn-action {
  background: #00adb5;
  color: white;
}

.btn-voice {
  background: #ff2e63;
  color: white;
}

#status {
  margin-top: 15px;
  font-size: 18px;
  font-weight: bold;
  color: #ff2e63;
}

</style>

</head>

<body>

<div class="container">

<h1>🚪 Smart Door Security</h1>

<textarea
id="cmdInput"
placeholder="Type command...">
</textarea>

<br>

<button
class="btn-action"
onclick="sendTextCmd()">
Submit Text
</button>

<button
id="voiceBtn"
class="btn-voice"
onclick="startSpeechRecognition()">
🎤 Voice Command
</button>

<div id="status">
Status: Secured 🔒
</div>

</div>

<script>

function startSpeechRecognition()
{
  const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;

  if (!SpeechRecognition)
  {
    alert("Voice not supported.");
    return;
  }

  const recognition =
    new SpeechRecognition();

  recognition.lang = 'en-US';

  recognition.onresult =
    (event) =>
    {
      const transcript =
        event.results[0][0].transcript;

      document.getElementById(
        "cmdInput"
      ).value = transcript;

      processCommand(transcript);
    };

  recognition.start();
}

function sendTextCmd()
{
  const txt =
    document.getElementById(
      "cmdInput"
    ).value;

  if (txt.trim())
  {
    processCommand(txt);
  }
}

function processCommand(cmdText)
{
  const cmd =
    cmdText.toLowerCase();

  let action = "";

  if (
    cmd.includes("open") ||
    cmd.includes("unlock")
  )
  {
    action = "unlock";

    document.getElementById(
      "status"
    ).innerHTML =
      "Status: UNLOCKED 🔓";

    document.getElementById(
      "status"
    ).style.color = "#4caf50";
  }

  else if (
    cmd.includes("close") ||
    cmd.includes("lock")
  )
  {
    action = "lock";

    document.getElementById(
      "status"
    ).innerHTML =
      "Status: Secured 🔒";

    document.getElementById(
      "status"
    ).style.color = "#ff2e63";
  }

  if (action !== "")
  {
    fetch('/execute?action=' + action);
  }
}

</script>

</body>

</html>

)rawliteral";

// ==========================================
// 🌐 ROOT PAGE
// ==========================================

void handleRoot()
{
  server.send(
    200,
    "text/html",
    index_html
  );
}

// ==========================================
// 🌐 EXECUTE COMMAND
// ==========================================

void handleExecute()
{
  if (server.hasArg("action"))
  {
    String action =
      server.arg("action");

    if (action == "unlock")
    {
      unlockDoor();
    }

    else if (action == "lock")
    {
      lockDoor();
    }
  }

  server.send(
    200,
    "text/plain",
    "OK"
  );
}

// ==========================================
// 🚀 SETUP
// ==========================================

void setup()
{
  Serial.begin(115200);

  delay(1000);

  Serial.println();
  Serial.println("================================");
  Serial.println("SMART DOOR SECURITY SYSTEM");
  Serial.println("================================");

  // ==========================================
  // GPIO SETUP
  // ==========================================

  pinMode(greenLed, OUTPUT);
  pinMode(redLed, OUTPUT);

  pinMode(
    vibrationPin,
    INPUT
  );

  // ==========================================
  // SERVO
  // ==========================================

  doorServo.attach(
    servoPin
  );

  lockDoor();

  // ==========================================
  // WIFI
  // ==========================================

  Serial.println();
  Serial.println("Connecting to WiFi...");

  WiFi.mode(WIFI_STA);

  WiFi.begin(
    ssid,
    password
  );

  while (
    WiFi.status() != WL_CONNECTED
  )
  {
    delay(500);

    Serial.print(".");
  }

  Serial.println();
  Serial.println("✅ WiFi connected!");

  Serial.print("ESP32 IP Address: ");
  Serial.println(
    WiFi.localIP()
  );

  Serial.print("WiFi RSSI: ");
  Serial.println(
    WiFi.RSSI()
  );

  // ==========================================
  // WEB SERVER
  // ==========================================

  server.on(
    "/",
    handleRoot
  );

  server.on(
    "/execute",
    handleExecute
  );

  server.begin();

  Serial.println(
    "✅ Web server started."
  );

  Serial.println();
  Serial.println(
    "SMART DOOR SYSTEM READY"
  );

  Serial.println(
    "================================"
  );
}

// ==========================================
// 🔄 MAIN LOOP
// ==========================================

void loop()
{
  server.handleClient();

  // ==========================================
  // VIBRATION DETECTION
  // ==========================================

  int vibrationState =
    digitalRead(
      vibrationPin
    );

  if (vibrationState == HIGH)
  {
    unsigned long currentTime =
      millis();

    // ==========================================
    // SENSOR DEBOUNCE
    // ==========================================

    if (
      currentTime -
      lastVibrationTime <
      vibrationDebounce
    )
    {
      return;
    }

    lastVibrationTime =
      currentTime;

    // ==========================================
    // ALERT COOLDOWN
    // ==========================================

    if (
      currentTime -
      lastAlertTime >=
      alertCooldown
    )
    {
      Serial.println();
      Serial.println(
        "⚠️ ALERT: Security breach detected!"
      );

      Serial.println(
        "Strong vibration detected on door."
      );

      // ========================================
      // SEND TELEGRAM
      // ========================================

      bool sent =
        sendTelegramAlert(
          "EMERGENCY: Someone is trying to break your door lock!"
        );

      if (sent)
      {
        Serial.println(
          "📲 Security alert delivered."
        );
      }
      else
      {
        Serial.println(
          "❌ Security alert could not be delivered."
        );
      }

      // Start cooldown regardless of result
      lastAlertTime =
        currentTime;
    }
  }
}