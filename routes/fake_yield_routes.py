from flask import Blueprint, request, jsonify
import json
import os
import uuid
from datetime import datetime

fake_bp = Blueprint('fake_yield', __name__)
DATA_FILE = os.path.join(os.path.dirname(__file__), '../data/dummy_store.json')

# Load existing data
def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

# Save data
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@fake_bp.route('/fake-yield', methods=['POST'])
def add_prediction():
    try:
        req = request.get_json()

        # Get values with defaults
        rainfall = req.get("rainfall")
        temperature = req.get("temperature")
        ph = req.get("ph")
        predicted_yield = req.get("predicted_yield")

        # ✅ Validation
        if rainfall is None or temperature is None or ph is None or predicted_yield is None:
            return jsonify({"error": "All fields are required (rainfall, temperature, ph, predicted_yield)."}), 400

        try:
            rainfall = float(rainfall)
            temperature = float(temperature)
            ph = float(ph)
            predicted_yield = float(predicted_yield)
        except ValueError:
            return jsonify({"error": "All fields must be numbers."}), 400

        if rainfall < 0:
            return jsonify({"error": "Rainfall cannot be negative."}), 400
        if not (0 <= ph <= 14):
            return jsonify({"error": "pH must be between 0 and 14."}), 400
        if predicted_yield < 0:
            return jsonify({"error": "Predicted yield must be non-negative."}), 400

        # Build and save record
        new_record = {
            "id": str(uuid.uuid4()),
            "rainfall": rainfall,
            "temperature": temperature,
            "ph": ph,
            "predicted_yield": predicted_yield,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        data = load_data()
        data.append(new_record)
        save_data(data)

        return jsonify({"message": "Data stored successfully!", "record": new_record}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@fake_bp.route('/fake-yield', methods=['GET'])
def get_all_predictions():
    data = load_data()
    return jsonify(data), 200

@fake_bp.route('/fake-yield/<string:record_id>', methods=['PUT'])
def update_prediction(record_id):
    try:
        req = request.get_json()

        # Load existing data
        data = load_data()

        # Find the record by ID
        record = next((r for r in data if r['id'] == record_id), None)

        if not record:
            return jsonify({"error": "Record not found."}), 404

        # Update fields if present in request
        for key in ['rainfall', 'temperature', 'ph', 'predicted_yield']:
            if key in req:
                record[key] = float(req[key])  # Convert to float

        # Update timestamp to show when it was modified
        record['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Save updated data
        save_data(data)

        return jsonify({"message": "Record updated successfully.", "record": record}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@fake_bp.route('/fake-yield/<string:record_id>', methods=['DELETE'])
def delete_prediction(record_id):
    try:
        data = load_data()

        # Find the index of the record
        record_index = next((i for i, r in enumerate(data) if r['id'] == record_id), None)

        if record_index is None:
            return jsonify({"error": "Record not found."}), 404

        # Remove the record
        deleted_record = data.pop(record_index)
        save_data(data)

        return jsonify({"message": "Record deleted successfully.", "record": deleted_record}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
