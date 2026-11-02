
import serial
import time


class RobotSerial:
    def __init__(self, port, baud_rate):
        self.connection = serial.Serial(
            port=port,
            baudrate=baud_rate,
            timeout=1,
            write_timeout=1
        )

        # ESP32 may restart when serial opens.
        time.sleep(2)
        self.last_command = None

        # Start safely
        self.send("STOP")

    def send(self, command):
        allowed = {
            "FWD", "BACK", "LEFT", "RIGHT", "STOP"
        }

        if command not in allowed:
            return

        if command != self.last_command:
            self.connection.write(
                (command + "\n").encode("ascii")
            )
            self.connection.flush()
            print("Robot command:", command)
            self.last_command = command

    def close(self):
        try:
            self.send("STOP")
            time.sleep(0.1)
        finally:
            self.connection.close()
