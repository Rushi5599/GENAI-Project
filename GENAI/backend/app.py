from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

# =========================================================
# PATH SETUP
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# backend/
#    app.py
#    data/
#
# frontend/
#    home.html
#    home.css
#    home.js
#    etc.
#
# So frontend is one level above backend.
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")


# =========================================================
# APP SETUP
# =========================================================

app = Flask(
    __name__,
    static_folder=FRONTEND_DIR,
    static_url_path=""
)

CORS(app)


# =========================================================
# JSON DATA LOADER
# =========================================================

def load_json(filename):
    path = os.path.join(BASE_DIR, "data", filename)

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# =========================================================
# AI IMPORTS
# =========================================================

from ai.customer_booking_ai import recommend_truck
from ai.driverinterface_ai import suggest_route
from ai.reduce_empty_ai import reduce_empty_trips
from ai.emergency_customer_ai import handle_emergency
from ai.driver_emergency_ai import handle_driver_emergency
from ai.owener_ai import analyze_owner
from ai.home_ai import home_summary


# =========================================================
# HOME / FRONTEND
# =========================================================

@app.route("/")
def home():
    return app.send_static_file("home.html")


# =========================================================
# AI CHAT
# =========================================================

@app.route("/ai/chat", methods=["POST"])
def chat_ai():

    data = request.json or {}

    role = data.get("role", "customer")
    msg = data.get("message", "").lower()

    if role == "customer":

        reply = (
            "I can help you book trucks, estimate cost, "
            "and suggest the best vehicle for your load."
        )

    elif role == "driver":

        reply = (
            "I assist with route guidance, emergencies, "
            "and reducing empty trips."
        )

    elif role == "owner":

        reply = (
            "I provide fleet analytics, utilization tips, "
            "and cost optimization insights."
        )

    else:

        reply = "How can I help you?"

    if "cost" in msg:

        reply += (
            " Estimated cost depends on distance, "
            "weight, and truck type."
        )

    if "emergency" in msg:

        reply += (
            " You can report emergencies "
            "from the Emergency section."
        )

    return jsonify({
        "reply": reply
    })


# =========================================================
# CUSTOMER BOOKING
# =========================================================

@app.route("/ai/customer", methods=["POST"])
def customer_booking():

    data = request.json or {}

    try:

        trucks = load_json("trucks.json")
        routes = load_json("routes.json")

        from_city = data["from"].strip().title()
        to_city = data["to"].strip().title()

        route_key = f"{from_city}-{to_city}"

        distance = routes.get(route_key, 100)

        result = recommend_truck(
            data["loadType"],
            float(data["weight"]),
            distance,
            trucks
        )

        return jsonify(result)

    except KeyError as e:

        return jsonify({
            "error": f"Missing field: {str(e)}"
        }), 400

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# =========================================================
# DRIVER ROUTE
# =========================================================

@app.route("/ai/driver-route", methods=["POST"])
def driver_route():

    data = request.json or {}

    try:

        routes = load_json("routes.json")

        result = suggest_route(
            data["from"],
            data["to"],
            routes
        )

        return jsonify(result)

    except KeyError as e:

        return jsonify({
            "error": f"Missing field: {str(e)}"
        }), 400

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# =========================================================
# REDUCE EMPTY TRIPS
# =========================================================

@app.route("/ai/reduce-empty", methods=["POST"])
def reduce_empty():

    data = request.json or {}

    location = data.get("location")

    if not location:

        return jsonify({
            "error": "location is required"
        }), 400

    try:

        loads = load_json("return_loads.json")

        result = reduce_empty_trips(
            location,
            loads
        )

        return jsonify(result)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# =========================================================
# CUSTOMER EMERGENCY
# =========================================================

@app.route("/ai/emergency", methods=["POST"])
def emergency_customer():

    data = request.json or {}

    try:

        resources = load_json(
            "emergency_resources.json"
        )

        result = handle_emergency(
            data["loadType"],
            data["from"],
            data["to"],
            resources
        )

        return jsonify(result)

    except KeyError as e:

        return jsonify({
            "error": f"Missing field: {str(e)}"
        }), 400

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# =========================================================
# DRIVER EMERGENCY
# =========================================================

@app.route("/ai/driver-emergency", methods=["POST"])
def driver_emergency():

    data = request.json or {}

    emergency_type = data.get("emergencyType")
    location = data.get("location")

    if not emergency_type or not location:

        return jsonify({
            "error": "emergencyType and location are required"
        }), 400

    try:

        rules = load_json(
            "driver_emergency_rules.json"
        )

        result = handle_driver_emergency(
            emergency_type,
            location,
            rules
        )

        return jsonify(result)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# =========================================================
# OWNER DASHBOARD
# =========================================================

@app.route("/owner-ai", methods=["POST"])
def owner_dashboard():

    data = request.json or {}

    fleet = data.get(
        "fleet",
        "Unknown"
    )

    location = data.get(
        "location",
        "Unknown"
    )

    status = data.get(
        "status",
        "idle"
    )

    try:

        rules = load_json(
            "owner_rules.json"
        )

        result = analyze_owner(
            fleet,
            location,
            status,
            rules
        )

        return jsonify(result)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# =========================================================
# SERVER
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )