
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// ==========================================
// MUSKAN HARDWARE CONFIGURATION
// ==========================================

#define OLED_SDA 4
#define OLED_SCL 15
#define OLED_ADDR 0x3C
#define BUTTON_PIN 27

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

// A 128x64 monochrome bitmap contains 1024 bytes.
// Hex encoding requires 2048 characters.
#define BITMAP_BYTES 1024
#define BITMAP_HEX_LENGTH 2048
#define MAX_SERIAL_LENGTH 2200

Adafruit_SSD1306 display(
  SCREEN_WIDTH,
  SCREEN_HEIGHT,
  &Wire,
  -1
);

bool oledReady = false;
bool previousButtonState = HIGH;
unsigned long lastButtonTime = 0;

String serialLine = "";


// ==========================================
// NORMAL ENGLISH STATUS DISPLAY
// ==========================================

void showDisplay(String line1, String line2) {
  if (!oledReady) {
    Serial.println("OLED_ERROR");
    return;
  }

  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(1);
  display.setTextWrap(false);

  if (line1.length() > 21) {
    line1 = line1.substring(0, 21);
  }

  if (line2.length() > 21) {
    line2 = line2.substring(0, 21);
  }

  display.setCursor(0, 8);
  display.print(line1);

  display.setCursor(0, 32);
  display.print(line2);

  display.display();
}


// ==========================================
// HEX CONVERSION
// ==========================================

int hexValue(char c) {
  if (c >= '0' && c <= '9') {
    return c - '0';
  }

  if (c >= 'A' && c <= 'F') {
    return c - 'A' + 10;
  }

  if (c >= 'a' && c <= 'f') {
    return c - 'a' + 10;
  }

  return -1;
}


// ==========================================
// RECEIVE AND DISPLAY BITMAP
// ==========================================

void processBitmapCommand(const String &command) {
  const int prefixLength = 7;  // "BITMAP|"

  if (command.length() != prefixLength + BITMAP_HEX_LENGTH) {
    Serial.println("BITMAP_ERROR: Incorrect length");
    return;
  }

  uint8_t bitmap[BITMAP_BYTES];

  for (int i = 0; i < BITMAP_BYTES; i++) {
    int position = prefixLength + (i * 2);

    int highNibble = hexValue(command[position]);
    int lowNibble = hexValue(command[position + 1]);

    if (highNibble < 0 || lowNibble < 0) {
      Serial.println("BITMAP_ERROR: Invalid hex data");
      return;
    }

    bitmap[i] = (highNibble << 4) | lowNibble;
  }

  if (!oledReady) {
    Serial.println("OLED_ERROR: Display not initialized");
    return;
  }

  display.clearDisplay();

  display.drawBitmap(
    0,
    0,
    bitmap,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SSD1306_WHITE
  );

  display.display();

  Serial.println("OLED_OK");
}


// ==========================================
// SERIAL COMMAND HANDLER
// ==========================================

void processSerialCommand(String command) {
  command.trim();

  if (command.startsWith("BITMAP|")) {
    processBitmapCommand(command);
    return;
  }

  // Keep compatibility with the old two-line command.
  if (command.startsWith("DISPLAY|")) {
    int separator = command.indexOf('|', 8);

    if (separator < 0) {
      Serial.println("DISPLAY_ERROR: Missing separator");
      return;
    }

    String line1 = command.substring(8, separator);
    String line2 = command.substring(separator + 1);

    showDisplay(line1, line2);
    Serial.println("OLED_OK");
    return;
  }

  if (command.length() > 0) {
    Serial.print("UNKNOWN_SERIAL_COMMAND: ");
    Serial.println(command);
  }
}


// ==========================================
// SETUP
// ==========================================

void setup() {
  Serial.begin(115200);

  pinMode(BUTTON_PIN, INPUT_PULLUP);

  Wire.begin(OLED_SDA, OLED_SCL);
  Wire.setClock(100000);

  oledReady = display.begin(
    SSD1306_SWITCHCAPVCC,
    OLED_ADDR
  );

  if (!oledReady) {
    Serial.println("OLED_ERROR: Check wiring and address");
  } else {
    showDisplay("MUSKAN AI", "Starting...");
    delay(1000);

    showDisplay("MUSKAN READY", "Press button");
  }

  Serial.println("MUSKAN_HARDWARE_READY");
}


// ==========================================
// MAIN LOOP
// ==========================================

void loop() {
  while (Serial.available() > 0) {
    char c = (char)Serial.read();

    if (c == '\n') {
      processSerialCommand(serialLine);
      serialLine = "";
    } else if (c != '\r') {
      if (serialLine.length() < MAX_SERIAL_LENGTH) {
        serialLine += c;
      } else {
        serialLine = "";
        Serial.println("SERIAL_ERROR: Command too long");
      }
    }
  }

  bool currentButtonState = digitalRead(BUTTON_PIN);

  if (
    previousButtonState == HIGH &&
    currentButtonState == LOW &&
    millis() - lastButtonTime > 350
  ) {
    lastButtonTime = millis();

    showDisplay("MUSKAN", "Listening...");
    Serial.println("BUTTON");
  }

  previousButtonState = currentButtonState;

  delay(5);
}
