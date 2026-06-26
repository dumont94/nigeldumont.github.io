"""
app.py — Flask API for the SOHO Network Builder.

Routes:
  GET  /api/health     — liveness check (useful for Docker/k8s health probes)
  POST /api/recommend  — accepts questionnaire answers, returns full build plan

Design decisions:
  - CORS is enabled for all origins in development. In production, restrict
    origins to your actual domain via the CORS_ORIGINS env var.
  - All recommendation logic lives in recommendations.py, not here.
    This file is intentionally thin — just HTTP plumbing.
  - No database. All state lives in the request/response cycle.
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS

from recommendations import (
    build_recommendation,
    VALID_BUSINESS_TYPES,
    VALID_SIZES,
    VALID_BUDGETS,
    VALID_MANAGEMENT_STYLES,
)

app = Flask(__name__)

# Allow the React dev server (localhost:5173) to call this API.
# In production, set CORS_ORIGINS to your actual frontend domain.
cors_origins = os.environ.get("CORS_ORIGINS", "*")
CORS(app, origins=cors_origins)


@app.route("/api/health")
def health():
    """Simple liveness check — returns 200 if the server is running."""
    return jsonify({"status": "ok"})


@app.route("/api/recommend", methods=["POST"])
def recommend():
    """
    Accept questionnaire answers and return a complete network build plan.

    Request body (JSON):
      {
        "business_type":    "startup",
        "size":             "1-10" | "11-50" | "51+",
        "budget":           "budget_conscious" | "enterprise",
        "management_style": "diy" | "outsourced"
      }

    Response (JSON):
      {
        "path":      "budget_diy" | "enterprise_diy" | "outsourced",
        "path_info": { name, tagline, audience, year1_cost, recurring_cost, description },
        "steps":     [ { id, order, title, icon, what, why, products, alternatives,
                         patching_notes, config_steps } × 10 ],
        "sources":   [ { vendor, url, note } × 7 ],
        "inputs":    { original questionnaire answers }
      }
    """
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must be JSON."}), 400

    # Validate all required fields are present
    required_fields = ["business_type", "size", "budget", "management_style"]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    # Validate field values against the allowed set
    validation_errors = []
    if data["business_type"] not in VALID_BUSINESS_TYPES:
        validation_errors.append(f"business_type must be one of: {VALID_BUSINESS_TYPES}")
    if data["size"] not in VALID_SIZES:
        validation_errors.append(f"size must be one of: {VALID_SIZES}")
    if data["budget"] not in VALID_BUDGETS:
        validation_errors.append(f"budget must be one of: {VALID_BUDGETS}")
    if data["management_style"] not in VALID_MANAGEMENT_STYLES:
        validation_errors.append(f"management_style must be one of: {VALID_MANAGEMENT_STYLES}")

    if validation_errors:
        return jsonify({"error": "Invalid field values.", "details": validation_errors}), 400

    result = build_recommendation(
        business_type=data["business_type"],
        size=data["size"],
        budget=data["budget"],
        management_style=data["management_style"],
    )

    return jsonify(result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "true").lower() == "true"
    app.run(debug=debug, port=port)
