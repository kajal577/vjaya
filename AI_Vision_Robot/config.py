
# Change COM port to the port shown in Arduino IDE.
SERIAL_PORT = "COM4"
BAUD_RATE = 115200

CAMERA_INDEX = 0

# Face-following settings
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Face width in pixels:
# below this -> approach
# above this -> move back
MIN_FACE_WIDTH = 100
MAX_FACE_WIDTH = 190

# Dead zone around the middle of the image
CENTER_TOLERANCE = 65

# Set False to test the camera without moving motors.
ENABLE_MOTORS = True
