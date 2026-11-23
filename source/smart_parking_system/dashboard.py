
"""
============================================================
VJaYa Robotics
PROJECT 07: SMART PARKING SYSTEM
File: dashboard.py

Flask Smart Parking Management Dashboard
============================================================
"""

import logging
import sqlite3

from flask import Flask, render_template_string, jsonify

from config import DATABASE_PATH, TOTAL_PARKING_SLOTS

logger = logging.getLogger(__name__)

app = Flask(__name__)


# ------------------------------------------------------------
# DASHBOARD HTML
# ------------------------------------------------------------

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>VJaYa Robotics | Smart Parking</title>

    <meta http-equiv="refresh" content="10">

    <style>

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: Arial, sans-serif;
            background: #080d19;
            color: #ffffff;
            padding: 25px;
        }

        header {
            text-align: center;
            margin-bottom: 30px;
        }

        header h1 {
            color: #62e6c5;
            margin-bottom: 8px;
        }

        header p {
            color: #aab4c5;
        }

        .container {
            max-width: 1200px;
            margin: auto;
        }

        .stats {
            display: grid;
            grid-template-columns:
                repeat(auto-fit, minmax(200px, 1fr));
            gap: 18px;
            margin-bottom: 30px;
        }

        .card {
            background: #121c2e;
            padding: 25px;
            border-radius: 12px;
            border: 1px solid #26364d;
        }

        .card h3 {
            color: #aab4c5;
            margin-bottom: 15px;
        }

        .card h2 {
            color: #62e6c5;
            font-size: 32px;
        }

        .section-title {
            color: #62e6c5;
            margin-bottom: 18px;
        }

        .slots {
            display: grid;
            grid-template-columns:
                repeat(auto-fit, minmax(130px, 1fr));
            gap: 15px;
            margin-bottom: 35px;
        }

        .slot {
            padding: 22px 10px;
            text-align: center;
            border-radius: 10px;
            background: #173d32;
            border: 1px solid #287b60;
        }

        .slot.occupied {
            background: #49242b;
            border-color: #a74755;
        }

        .slot h3 {
            margin-bottom: 10px;
        }

        .slot p {
            font-size: 13px;
        }

        .table-wrapper {
            overflow-x: auto;
            background: #121c2e;
            border-radius: 12px;
            padding: 15px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            min-width: 650px;
        }

        th, td {
            padding: 14px;
            text-align: left;
            border-bottom: 1px solid #26364d;
        }

        th {
            color: #62e6c5;
        }

        td {
            color: #d5dbea;
        }

        .status {
            color: #62e6c5;
            font-weight: bold;
        }

        footer {
            text-align: center;
            color: #8290a5;
            margin-top: 35px;
        }

    </style>

</head>

<body>

<div class="container">

    <header>

        <h1>VJaYa Robotics</h1>

        <p>Smart Parking Management System</p>

    </header>

    <section class="stats">

        <div class="card">

            <h3>Total Slots</h3>

            <h2>{{ total_slots }}</h2>

        </div>

        <div class="card">

            <h3>Occupied Slots</h3>

            <h2>{{ occupied_slots }}</h2>

        </div>

        <div class="card">

            <h3>Available Slots</h3>

            <h2>{{ available_slots }}</h2>

        </div>

        <div class="card">

            <h3>Parked Vehicles</h3>

            <h2>{{ parked_count }}</h2>

        </div>

    </section>

    <h2 class="section-title">Parking Slot Status</h2>

    <section class="slots">

        {% for slot in slots %}

        <div class="slot
            {% if slot.status == 'OCCUPIED' %}occupied{% endif %}">

            <h3>{{ slot.name }}</h3>

            <p>{{ slot.status }}</p>

        </div>

        {% endfor %}

    </section>

    <h2 class="section-title">Currently Parked Vehicles</h2>

    <div class="table-wrapper">

        <table>

            <thead>

                <tr>
                    <th>Number Plate</th>
                    <th>Parking Slot</th>
                    <th>Entry Time</th>
                    <th>Status</th>
                </tr>

            </thead>

            <tbody>

                {% for vehicle in vehicles %}

                <tr>

                    <td>{{ vehicle.plate_number }}</td>

                    <td>{{ vehicle.parking_slot }}</td>

                    <td>{{ vehicle.entry_time }}</td>

                    <td class="status">{{ vehicle.status }}</td>

                </tr>

                {% else %}

                <tr>
                    <td colspan="4">No vehicles currently parked.</td>
                </tr>

                {% endfor %}

            </tbody>

        </table>

    </div>

    <footer>

        VJaYa Robotics | Smart Parking System

    </footer>

</div>

</body>
</html>
"""


# ------------------------------------------------------------
# DATABASE CONNECTION
# ------------------------------------------------------------

def get_database_connection():

    connection = sqlite3.connect(
        str(DATABASE_PATH),
        timeout=10
    )

    connection.row_factory = sqlite3.Row

    return connection


# ------------------------------------------------------------
# GET DASHBOARD DATA
# ------------------------------------------------------------

def get_dashboard_data():

    connection = get_database_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                parking_slot,
                COUNT(*) AS vehicle_count
            FROM vehicles
            WHERE status = 'PARKED'
            GROUP BY parking_slot
        """)

        occupied_data = cursor.fetchall()

        occupied_slot_names = {
            row["parking_slot"]
            for row in occupied_data
            if row["parking_slot"] is not None
        }

        slots = []

        for number in range(1, TOTAL_PARKING_SLOTS + 1):

            slot_name = f"P{number}"

            status = (
                "OCCUPIED"
                if slot_name in occupied_slot_names
                else "AVAILABLE"
            )

            slots.append({
                "name": slot_name,
                "status": status
            })

        cursor.execute("""
            SELECT
                plate_number,
                parking_slot,
                entry_time,
                status
            FROM vehicles
            WHERE status = 'PARKED'
            ORDER BY entry_time DESC
        """)

        vehicles = [
            dict(row)
            for row in cursor.fetchall()
        ]

        occupied_slots = sum(
            1 for slot in slots
            if slot["status"] == "OCCUPIED"
        )

        available_slots = (
            TOTAL_PARKING_SLOTS - occupied_slots
        )

        return {
            "total_slots": TOTAL_PARKING_SLOTS,
            "occupied_slots": occupied_slots,
            "available_slots": available_slots,
            "parked_count": len(vehicles),
            "slots": slots,
            "vehicles": vehicles
        }

    finally:

        connection.close()


# ------------------------------------------------------------
# MAIN DASHBOARD PAGE
# ------------------------------------------------------------

@app.route("/")

def dashboard():

    try:

        data = get_dashboard_data()

        return render_template_string(
            DASHBOARD_HTML,
            **data
        )

    except sqlite3.Error:

        logger.exception(
            "Unable to load parking dashboard."
        )

        return (
            "Database error. Please check the parking database.",
            500
        )


# ------------------------------------------------------------
# DASHBOARD DATA API
# ------------------------------------------------------------

@app.route("/api/dashboard")

def dashboard_api():

    try:

        return jsonify(
            get_dashboard_data()
        )

    except sqlite3.Error:

        logger.exception(
            "Dashboard API database error."
        )

        return jsonify({
            "success": False,
            "error": "Database unavailable"
        }), 500


# ------------------------------------------------------------
# START DASHBOARD SERVER
# ------------------------------------------------------------

def start_dashboard(
    host="0.0.0.0",
    port=5000,
    debug=False
):

    logger.info(
        "Starting Smart Parking Dashboard on port %s",
        port
    )

    app.run(
        host=host,
        port=port,
        debug=debug,
        use_reloader=False,
        threaded=True
    )


# ------------------------------------------------------------
# DIRECT EXECUTION
# ------------------------------------------------------------

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    start_dashboard()
