import json
import sys
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

from typing import Tuple

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

def calculate_bmi(weight_kg: float, height_m: float) -> float:

    if height_m <= 0 or weight_kg <= 0:
        raise ValueError("Weight and height must be positive numbers")
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)


def calculate_bmi_from_ft_in(weight_kg: float, height_ft: float, height_in: float) -> float:
    """Calculate BMI given weight in kg and height in feet + inches.

    Conversion: total_inches = (ft * 12) + in
    height_m = total_inches * 0.0254
    """
    if weight_kg <= 0:
        raise ValueError("Weight must be positive")
    # allow zero ft if inches provided
    total_inches = (float(height_ft) * 12.0) + float(height_in)
    if total_inches <= 0:
        raise ValueError("Height must be positive")
    height_m = total_inches * 0.0254
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)


def categorize_bmi(bmi: float) -> Tuple[str, str]:

    if bmi < 18.5:
        return "Underweight", "#FF8C00"  # Orange
    if 18.5 <= bmi <= 25:
        return "Normal", "#2ECC71"  # Green
    if 25 < bmi <= 30:
        return "Overweight", "#3498DB"  # Blue
    return "Obese", "#E74C3C"  # Red


app = Flask(__name__, static_folder=str(ROOT / "frontend"), static_url_path="")


@app.route("/api/bmi", methods=["POST"])
def api_bmi():
    data = request.get_json() or {}
    # Accept either weight_kg or weight_lb
    weight = None
    if "weight_kg" in data:
        weight = float(data["weight_kg"])
    elif "weight_lb" in data:
        weight = float(data["weight_lb"]) * 0.45359237

    # Height: prefer explicit feet+inches when provided, otherwise accept height_m or decimal feet
    height_m = None
    use_ft_in = False
    if ("height_ft" in data) or ("height_in" in data):
        ft = float(data.get("height_ft", 0))
        inch = float(data.get("height_in", 0))
        use_ft_in = True
    elif "height_m" in data:
        # only use height_m when ft/in not supplied
        height_m = float(data["height_m"])
    elif "height_ft" in data:
        # decimal feet (single field like 5.75 ft)
        height_m = float(data["height_ft"]) / 3.28084

    if weight is None:
        return jsonify({"error": "weight required (weight_kg or weight_lb)"}), 400

    used = 'unknown'
    try:
        if use_ft_in:
            # calculate using ft + in conversion
            ft = float(data.get("height_ft", 0))
            inch = float(data.get("height_in", 0))
            bmi_val = calculate_bmi_from_ft_in(weight, ft, inch)
            used = 'ft_in'
        else:
            if height_m is None:
                return jsonify({"error": "height required (height_m or height_ft/height_in)"}), 400
            bmi_val = calculate_bmi(weight, height_m)
            used = 'metric'
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    cat, color = categorize_bmi(bmi_val)
    # match the user-facing message format: "You are in the '<category>' category."
    msg = f"Your BMI is {bmi_val} - You are in the '{cat}' category."
    # include which height parsing was used for debugging
    return jsonify({"bmi": bmi_val, "category": cat, "color": color, "message": msg, "used": used})


@app.route("/", methods=["GET"])
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)


def main():
    # Run on localhost only
    app.run(host="127.0.0.1", port=5000, debug=False)


if __name__ == "__main__":
    main()
