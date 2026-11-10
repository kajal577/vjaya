import serial
import time

from config import BLUETOOTH_PORT, BLUETOOTH_BAUDRATE


class BluetoothLink:

    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = serial.Serial(
                BLUETOOTH_PORT,
                BLUETOOTH_BAUDRATE,
                timeout=1
            )

            time.sleep(2)
            print("Bluetooth connected!")

            return True

        except serial.SerialException as error:
            print("Bluetooth connection failed:", error)
            return False

    def send(self, command):
        if self.connection and self.connection.is_open:
            self.connection.write(command.encode("utf-8"))

    def disconnect(self):
        if self.connection and self.connection.is_open:
            self.send("S")
            self.connection.close()
            print("Bluetooth disconnected.")