from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# In-memory order store (replace with DB in production)
orders = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "saota-venture"})

@app.route("/api/book", methods=["POST"])
def book():
    data = request.get_json() or {}
    required = ["name", "phone", "service", "address"]
    for field in required:
        if not data.get(field, "").strip():
            return jsonify({"success": False, "error": f"{field} is required."}), 400
    order = {
        "id": f"SAO{len(orders)+1001}",
        "name": data["name"].strip(),
        "phone": data["phone"].strip(),
        "email": data.get("email", "").strip(),
        "service": data["service"].strip(),
        "capacity": data.get("capacity", "").strip(),
        "address": data["address"].strip(),
        "area": data.get("area", "").strip(),
        "notes": data.get("notes", "").strip(),
        "status": "pending",
        "created": datetime.utcnow().isoformat()
    }
    orders.append(order)
    print(f"[ORDER] {order}")
    return jsonify({
        "success": True,
        "message": f"Order received! Your booking ID is {order['id']}. We'll call you within 30 minutes.",
        "order_id": order["id"]
    })

@app.route("/api/orders")
def get_orders():
    return jsonify({"orders": orders, "total": len(orders)})

@app.route("/api/contact", methods=["POST"])
def contact():
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()
    if not name or not message:
        return jsonify({"success": False, "error": "Name and message are required."}), 400
    print(f"[CONTACT] {name} <{email}>: {message}")
    return jsonify({"success": True, "message": "Message received! We'll respond within 24 hours."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") != "production"
    app.run(host="0.0.0.0", port=port, debug=debug)
