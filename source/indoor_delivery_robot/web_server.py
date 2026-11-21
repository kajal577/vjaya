
"""
INDOOR DELIVERY ROBOT
File: web_server.py

Flask web interface for delivery control.
"""

import threading

from flask import Flask, jsonify, request, render_template_string

import config
import delivery
import navigation


app = Flask(__name__)

_delivery_thread = None
_delivery_lock = threading.Lock()

_status = {
    "state": "IDLE",
    "destination": None,
    "message": "Robot ready."
}


HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>Indoor Delivery Robot</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            padding: 20px;
            font-family: Arial, sans-serif;
            background: #101827;
            color: #ffffff;
        }

        .container {
            max-width: 600px;
            margin: auto;
        }

        h1 {
            text-align: center;
            color: #62e6c5;
        }

        .card {
            background: #1b2638;
            padding: 20px;
            margin-top: 18px;
            border-radius: 14px;
        }

        .status {
            font-size: 18px;
            font-weight: bold;
            color: #62e6c5;
        }

        select, button {
            width: 100%;
            padding: 14px;
            margin-top: 12px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
        }

        select {
            background: #ffffff;
            color: #111827;
        }

        button {
            background: #62e6c5;
            color: #101827;
            font-weight: bold;
            cursor: pointer;
        }

        button:hover {
            opacity: 0.9;
        }

        .home {
            background: #8ca7ff;
        }

        .stop {
            background: #ff5f65;
            color: #ffffff;
        }

        .message {
            margin-top: 12px;
            color: #cbd5e1;
            min-height: 24px;
        }

        .small {
            color: #9ca3af;
            font-size: 13px;
            line-height: 1.5;
        }
    </style>
</head>

<body>
<div class="container">

    <h1>Indoor Delivery Robot</h1>

    <div class="card">
        <h2>Robot Status</h2>

        <p>State:
            <span class="status" id="state">Loading...</span>
        </p>

        <p>Destination:
            <span id="destination">None</span>
        </p>

        <p id="statusMessage">Connecting to robot...</p>
    </div>

    <div class="card">
        <h2>Send Delivery</h2>

        <label for="room">Select destination:</label>

        <select id="room">
            {% for room in rooms %}
            <option value="{{ room }}">{{ room }}</option>
            {% endfor %}
        </select>

        <button onclick="startDelivery()">
            Start Delivery
        </button>

        <button class="home" onclick="returnHome()">
            Return Home
        </button>

        <button class="stop" onclick="cancelDelivery()">
            STOP ROBOT
        </button>

        <p class="message" id="message"></p>
    </div>

    <div class="card">
        <h2>Instructions</h2>

        <p class="small">
            Select a room and press Start Delivery.
            Keep the robot's path clear.
            Use STOP ROBOT if you need to interrupt movement.
        </p>
    </div>

</div>

<script>
async function sendCommand(url, data = {}) {
    const message = document.getElementById("message");

    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        message.textContent = result.message;

    } catch (error) {
        message.textContent = "Cannot connect to robot.";
    }
}

function startDelivery() {
    const room = document.getElementById("room").value;

    sendCommand("/api/delivery", {
        destination: room
    });
}

function returnHome() {
    sendCommand("/api/home");
}

function cancelDelivery() {
    sendCommand("/api/cancel");
}

async function updateStatus() {
    try {
        const response = await fetch("/api/status");
        const data = await response.json();

        document.getElementById("state").textContent =
            data.state;

        document.getElementById("destination").textContent =
            data.destination || "None";

        document.getElementById("statusMessage").textContent =
            data.message;

    } catch (error) {
        document.getElementById("state").textContent =
            "Disconnected";
    }
}

setInterval(updateStatus, 1000);
updateStatus();
</script>

</body>
</html>
"""


def _run_delivery(destination):
    """
    Run delivery in a background thread.
    """
    global _status

    try:
        _status["state"] = "DELIVERING"
        _status["destination"] = destination
        _status["message"] = f"Delivering to {destination}..."

        success = delivery.start_delivery(destination)

        if success:
            _status["state"] = "ARRIVED"
            _status["message"] = f"Arrived at {destination}."
        else:
            _status["state"] = "STOPPED"
            _status["message"] = "Delivery stopped or failed."

    except Exception as error:
        navigation.stop()

        _status["state"] = "ERROR"
        _status["message"] = str(error)

    finally:
        with _delivery_lock:
            _status["destination"] = None


def _run_home():
    """
    Return robot home in a background thread.
    """
    global _status

    try:
        _status["state"] = "RETURNING"
        _status["destination"] = "HOME"
        _status["message"] = "Returning home..."

        success = delivery.return_home()

        if success:
            _status["state"] = "IDLE"
            _status["message"] = "Robot returned home."
        else:
            _status["state"] = "STOPPED"
            _status["message"] = "Return-home operation failed."

    except Exception as error:
        navigation.stop()

        _status["state"] = "ERROR"
        _status["message"] = str(error)

    finally:
        with _delivery_lock:
            _status["destination"] = None


@app.route("/")
def home_page():
    """
    Display the robot control panel.
    """
    rooms = delivery.get_destinations()

    return render_template_string(
        HTML_PAGE,
        rooms=rooms
    )


@app.route("/api/status", methods=["GET"])
def get_status():
    """
    Return current robot status.
    """
    return jsonify(_status)


@app.route("/api/delivery", methods=["POST"])
def start_delivery():
    """
    Start a delivery to the selected room.
    """
    global _delivery_thread

    data = request.get_json(silent=True) or {}
    destination = data.get("destination")

    if not destination:
        return jsonify({
            "success": False,
            "message": "Please select a destination."
        }), 400

    if destination not in config.DELIVERY_LOCATIONS:
        return jsonify({
            "success": False,
            "message": "Invalid destination."
        }), 400

    with _delivery_lock:
        if _delivery_thread is not None and _delivery_thread.is_alive():
            return jsonify({
                "success": False,
                "message": "Robot is already performing an operation."
            }), 409

        _delivery_thread = threading.Thread(
            target=_run_delivery,
            args=(destination,),
            daemon=True
        )

        _delivery_thread.start()

    return jsonify({
        "success": True,
        "message": f"Delivery to {destination} started."
    })


@app.route("/api/home", methods=["POST"])
def go_home():
    """
    Start return-home operation.
    """
    global _delivery_thread

    with _delivery_lock:
        if _delivery_thread is not None and _delivery_thread.is_alive():
            return jsonify({
                "success": False,
                "message": "Robot is already moving."
            }), 409

        _delivery_thread = threading.Thread(
            target=_run_home,
            daemon=True
        )

        _delivery_thread.start()

    return jsonify({
        "success": True,
        "message": "Return-home operation started."
    })


@app.route("/api/cancel", methods=["POST"])
def cancel():
    """
    Stop robot movement.
    """
    global _status

    navigation.stop()

    _status["state"] = "STOPPED"
    _status["message"] = "Stop command sent."

    return jsonify({
        "success": True,
        "message": "Stop command sent to robot."
    })


def run_server():
    """
    Start the Flask web server.
    """
    print("Indoor Delivery Robot Web Server")
    print(f"Open on this Pi: http://localhost:{config.WEB_PORT}")
    print("Use the Raspberry Pi's IP address on your phone.")

    app.run(
        host=config.WEB_HOST,
        port=config.WEB_PORT,
        debug=False,
        use_reloader=False
    )


if __name__ == "__main__":
    run_server()
