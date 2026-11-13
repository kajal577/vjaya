from bluetooth_link import BluetoothLink


class RobotControl:

    def __init__(self):
        self.bluetooth = BluetoothLink()

    def connect(self):
        return self.bluetooth.connect()

    def forward(self):
        self.bluetooth.send("F")

    def backward(self):
        self.bluetooth.send("B")

    def left(self):
        self.bluetooth.send("L")

    def right(self):
        self.bluetooth.send("R")

    def stop(self):
        self.bluetooth.send("S")

    def close(self):
        self.bluetooth.disconnect()