
#include <Arduino.h>

// L298N motor driver pins
const int IN1 = 16;
const int IN2 = 17;
const int IN3 = 18;
const int IN4 = 19;

const unsigned long COMMAND_TIMEOUT_MS = 1200;

String commandBuffer = "";
unsigned long lastCommandTime = 0;

void stopMotors() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}

void moveForward() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void moveBackward() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void turnLeft() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void turnRight() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void handleCommand(String command) {
  command.trim();
  command.toUpperCase();

  if (command == "FWD") {
    moveForward();
  } else if (command == "BACK") {
    moveBackward();
  } else if (command == "LEFT") {
    turnLeft();
  } else if (command == "RIGHT") {
    turnRight();
  } else if (command == "STOP") {
    stopMotors();
  } else {
    stopMotors();
    Serial.println("UNKNOWN COMMAND");
    return;
  }

  lastCommandTime = millis();
  Serial.print("ACK: ");
  Serial.println(command);
}

void setup() {
  Serial.begin(115200);

  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  stopMotors();
  lastCommandTime = millis();

  Serial.println("AI VISION ROBOT READY");
}

void loop() {
  while (Serial.available() > 0) {
    char c = (char)Serial.read();

    if (c == '\n') {
      handleCommand(commandBuffer);
      commandBuffer = "";
    } else if (c != '\r') {
      if (commandBuffer.length() < 32) {
        commandBuffer += c;
      } else {
        commandBuffer = "";
        stopMotors();
      }
    }
  }

  if (millis() - lastCommandTime > COMMAND_TIMEOUT_MS) {
    stopMotors();
  }
}
