import pandas as pd

def get_risk_level(probability):
    if probability < 0.40:
        return 'Low'
    elif probability < 0.70:
        return 'Medium'
    else:
        return 'High'

def predict(input_data, artifacts):
    model    = artifacts['model']
    scaler   = artifacts['scaler']
    features = artifacts['features']

    df = pd.DataFrame([input_data])
    df = df.reindex(columns=features, fill_value=0)

    X_scaled    = scaler.transform(df)
    probability = float(model.predict_proba(X_scaled)[0][1])
    risk_level  = get_risk_level(probability)

    return {'risk_level': risk_level, 'probability': round(probability, 4)}
