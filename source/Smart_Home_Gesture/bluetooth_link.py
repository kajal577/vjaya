
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
            print(f"Bluetooth connected on {BLUETOOTH_PORT}")

        except serial.SerialException as error:
            print("Bluetooth connection failed:", error)
            raise

    def send_command(self, command):
        if self.connection and self.connection.is_open:
            self.connection.write(command.encode("utf-8"))

    def close(self):
        if self.connection and self.connection.is_open:
            self.connection.close()
            print("Bluetooth disconnected.")
