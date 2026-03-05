import pickle
import json
import os

ARTIFACTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'dropout')

PATHS = {
    'model':    os.path.join(ARTIFACTS_DIR, 'dropout_model.pkl'),
    'scaler':   os.path.join(ARTIFACTS_DIR, 'scaler.pkl'),
    'encoders': os.path.join(ARTIFACTS_DIR, 'label_encoders.pkl'),
    'features': os.path.join(ARTIFACTS_DIR, 'feature_columns.json'),
}

def load_artifacts():
    try:
        with open(PATHS['model'],    'rb') as f: model    = pickle.load(f)
        with open(PATHS['scaler'],   'rb') as f: scaler   = pickle.load(f)
        with open(PATHS['encoders'], 'rb') as f: encoders = pickle.load(f)
        with open(PATHS['features'], 'r')  as f: features = json.load(f)
        return {'model': model, 'scaler': scaler, 'encoders': encoders, 'features': features}
    except FileNotFoundError as e:
        raise RuntimeError(f'Missing artifact file: {e.filename}')
