#include <Arduino.h>
#include <SoftwareSerial.h>

#include "config.h"
#include "bluetooth_control.h"

static SoftwareSerial btSerial(BT_RX, BT_TX);

static String input = "";

void initBluetooth() {

  btSerial.begin(BT_BAUD);

  Serial.println("BLUETOOTH READY");
}

BTCommand readBluetoothCommand(
  double &latitude,
  double &longitude
) {

  while (btSerial.available()) {

    char c = btSerial.read();

    if (c == '\n' || c == '\r') {

      if (input.length() == 0) {
        continue;
      }

      BTCommand command = BT_NONE;

      if (input == "STOP" || input == "CANCEL") {

        command = BT_STOP;
      }

      else if (input.startsWith("DEST,")) {

        int separator = input.indexOf(',', 5);

        if (separator > 5) {

          double lat = input.substring(
            5, separator
          ).toFloat();

          double lon = input.substring(
            separator + 1
          ).toFloat();

          if (lat >= -90 && lat <= 90 &&
              lon >= -180 && lon <= 180) {

            latitude = lat;
            longitude = lon;

            command = BT_DESTINATION;
          }
        }
      }

      input = "";

      return command;
    }

    else if (input.length() < 60) {

      input += c;
    }
    else {

      input = "";
    }
  }

  return BT_NONE;
}

void sendBluetoothMessage(const char *message) {

  btSerial.println(message);
}