
import cv2
import time
import threading

from flask import Flask, Response, jsonify, render_template_string

from config import DASHBOARD_HOST, DASHBOARD_PORT


HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Traffic Monitoring</title>

    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
        body {
            margin: 0;
            padding: 25px;
            background: #080d19;
            color: white;
            font-family: Arial, sans-serif;
        }

        h1 {
            color: #62e6c5;
        }

        .container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 15px;
        }

        .card {
            background: #151f31;
            padding: 20px;
            border-radius: 12px;
        }

        .value {
            font-size: 32px;
            color: #62e6c5;
        }

        img {
            width: 100%;
            max-width: 1000px;
            border-radius: 12px;
        }

        .video {
            margin-top: 25px;
        }
    </style>
</head>

<body>

<h1>AI Traffic Monitoring System</h1>

<div class="container">

    <div class="card">
        Total Vehicles
        <div class="value" id="total">0</div>
    </div>

    <div class="card">
        Cars
        <div class="value" id="cars">0</div>
    </div>

    <div class="card">
        Motorcycles
        <div class="value" id="motorcycles">0</div>
    </div>

    <div class="card">
        Buses
        <div class="value" id="buses">0</div>
    </div>

    <div class="card">
        Trucks
        <div class="value" id="trucks">0</div>
    </div>

    <div class="card">
        Congestion
        <div class="value" id="congestion">LOW</div>
    </div>

</div>

<div class="video">
    <h2>Live Traffic Camera</h2>
    <img src="/video_feed">
</div>

<script>

async function updateDashboard() {

    try {

        const response = await fetch("/api/stats");
        const data = await response.json();

        document.getElementById("total").innerText =
            data.vehicles_present;

        document.getElementById("cars").innerText =
            data.cars;

        document.getElementById("motorcycles").innerText =
            data.motorcycles;

        document.getElementById("buses").innerText =
            data.buses;

        document.getElementById("trucks").innerText =
            data.trucks;

        document.getElementById("congestion").innerText =
            data.congestion;

    } catch (error) {
        console.error(error);
    }
}

setInterval(updateDashboard, 1000);
updateDashboard();

</script>

</body>
</html>
"""


class TrafficDashboard:

    def __init__(self):

        self.app = Flask(__name__)

        self.frame = None
        self.statistics = {}
        self.lock = threading.Lock()

        self.register_routes()

    def register_routes(self):

        @self.app.route("/")
        def home():
            return render_template_string(HTML_PAGE)

        @self.app.route("/api/stats")
        def stats():

            with self.lock:
                return jsonify(self.statistics)

        @self.app.route("/video_feed")
        def video_feed():

            return Response(
                self.generate_frames(),
                mimetype="multipart/x-mixed-replace; boundary=frame"
            )

    def update(self, frame, statistics):

        with self.lock:

            self.frame = frame.copy()
            self.statistics = statistics.copy()

    def generate_frames(self):

        while True:

            with self.lock:

                frame = (
                    self.frame.copy()
                    if self.frame is not None
                    else None
                )

            if frame is None:
                time.sleep(0.1)
                continue

            success, encoded = cv2.imencode(
                ".jpg", frame
            )

            if not success:
                continue

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + encoded.tobytes()
                + b"\r\n"
            )

    def start(self):

        self.app.run(
            host=DASHBOARD_HOST,
            port=DASHBOARD_PORT,
            debug=False,
            threaded=True,
            use_reloader=False
        )
