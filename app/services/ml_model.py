import json
import joblib
import numpy as np
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "ml" / "model.pkl"
FEATURES_PATH = BASE_DIR / "ml" / "feature_columns.json"

model = joblib.load(MODEL_PATH)

with open(FEATURES_PATH, "r", encoding="utf-8") as f:
    feature_columns = json.load(f)


def prepare_features(data):
    runway = data.cash / data.burn_rate

    feature_map = {
        "cash": data.cash,
        "burn_rate": data.burn_rate,
        "runway": runway,
        "pmf_score": data.pmf_score,
        "retention_rate": data.retention_rate,
        "traction": data.traction,
        "adaptability": data.adaptability,
        "decision_delay": data.decision_delay,
        "team_strength": data.team_strength,
        "tech_debt": data.tech_debt,
        "scalability": data.scalability,
        "regulatory_risk": data.regulatory_risk,
        "external_shock": data.external_shock,
    }

    values = [feature_map[col] for col in feature_columns]
    return np.array(values).reshape(1, -1), feature_map


def predict_ai(data):
    X, feature_map = prepare_features(data)

    prediction = int(model.predict(X)[0])
    probabilities = model.predict_proba(X)[0]
    probability = float(probabilities[prediction])

    label = "FAILURE" if prediction == 1 else "SUCCESS"

    return {
        "prediction": prediction,
        "label": label,
        "probability": round(probability, 4),
        "runway": round(feature_map["runway"], 2),
        "feature_values": feature_map,
    }