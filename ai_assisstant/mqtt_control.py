
import ssl
import time
import paho.mqtt.client as mqtt
from config import (
    MQTT_HOST, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD
)

COMMAND_TOPIC = "muskan/device/command"
STATUS_TOPIC = "muskan/device/status"

_client = None
_connected = False

def mqtt_enabled():
    return (
        MQTT_HOST
        and "PASTE_YOUR_" not in MQTT_HOST
        and MQTT_USERNAME
        and "PASTE_YOUR_" not in MQTT_USERNAME
        and MQTT_PASSWORD
        and "PASTE_YOUR_" not in MQTT_PASSWORD
    )

def connect_mqtt():
    global _client, _connected

    if not mqtt_enabled():
        print("MQTT disabled: configure HiveMQ values in .env.")
        return False

    try:
        _client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            client_id=f"muskan-windows-{int(time.time())}"
        )
        _client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        _client.tls_set(cert_reqs=ssl.CERT_REQUIRED)
        _client.on_connect = _on_connect
        _client.on_disconnect = _on_disconnect
        _client.connect(MQTT_HOST, MQTT_PORT, keepalive=30)
        _client.loop_start()

        for _ in range(30):
            if _connected:
                return True
            time.sleep(0.2)
        print("MQTT connection timed out.")
        return False

    except Exception as exc:
        print("MQTT connection error:", exc)
        return False

def _on_connect(client, userdata, flags, reason_code, properties):
    global _connected
    _connected = (reason_code == 0)
    if _connected:
        print("MQTT connected to HiveMQ.")
        client.subscribe(STATUS_TOPIC)
    else:
        print("MQTT connection refused:", reason_code)

def _on_disconnect(client, userdata, disconnect_flags, reason_code, properties):
    global _connected
    _connected = False
    print("MQTT disconnected:", reason_code)

def send_device_command(command):
    if not _connected or _client is None:
        return "The ESP32 MQTT connection is not ready."

    allowed = {
        "LED ON", "LED OFF",
        "FAN1 ON", "FAN1 OFF",
        "FAN2 ON", "FAN2 OFF",
        "FAN ON", "FAN OFF",
        "GATE OPEN", "GATE CLOSE",
    }
    normalized = " ".join(command.upper().split())

    if normalized not in allowed:
        return "That device command is not allowed."

    info = _client.publish(COMMAND_TOPIC, normalized, qos=1)
    if info.rc != mqtt.MQTT_ERR_SUCCESS:
        return "I couldn't send the device command."

    return f"Command sent: {normalized}."

def disconnect_mqtt():
    global _client, _connected
    if _client is not None:
        _client.loop_stop()
        _client.disconnect()
    _client = None
    _connected = False
