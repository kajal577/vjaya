#include "bluetooth_control.h"
#include "balance_config.h"

static SoftwareSerial bluetooth(BT_RX, BT_TX);

static char movement = 'S';
static bool armed = false;

void initBluetooth() {
  bluetooth.begin(9600);
  movement = 'S';
  armed = false;
}

void readBluetooth() {
  while (bluetooth.available()) {
    char c = bluetooth.read();

    if (c >= 'a' && c <= 'z') c -= 32;

    if (c == 'A') {
      armed = true;
      movement = 'S';
    } else if (c == 'X') {
      armed = false;
      movement = 'S';
    } else if (c == 'F' || c == 'B' ||
               c == 'L' || c == 'R' || c == 'S') {
      movement = c;
    }
  }
}

char getMovementCommand() {
  return movement;
}

bool isArmed() {
  return armed;
}