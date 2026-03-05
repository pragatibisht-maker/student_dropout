from flask import Blueprint, request, jsonify, current_app
from utils.validator import validate_input
from utils.predictor import predict

predict_bp = Blueprint('predict', __name__)

@predict_bp.route('/predict', methods=['POST'])
def predict_dropout():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'error': 'Invalid or missing JSON body.'}), 400

    cleaned, errors = validate_input(data)
    if errors:
        return jsonify({'error': 'Validation failed.', 'details': errors}), 422

    try:
        artifacts = current_app.config['ARTIFACTS']
        result = predict(cleaned, artifacts)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': 'Prediction failed.', 'details': str(e)}), 500
