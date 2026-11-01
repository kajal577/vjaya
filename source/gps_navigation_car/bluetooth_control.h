#ifndef BLUETOOTH_CONTROL_H
#define BLUETOOTH_CONTROL_H

enum BTCommand {
  BT_NONE,
  BT_DESTINATION,
  BT_STOP
};

void initBluetooth();

BTCommand readBluetoothCommand(
  double &latitude,
  double &longitude
);

void sendBluetoothMessage(const char *message);

#endif