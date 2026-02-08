import os
import joblib
import pandas as pd
from cleanup_planner import generate_cleanup_plan

# Load trained model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "debris_model.pkl")
model = joblib.load(MODEL_PATH)

# Feature names
COLUMNS = ["semi_major_axis", "eccentricity", "inclination", "raan", "arg_perigee", "mean_anomaly"]

def predict_object(orbital_params_dict):
    """
    Predicts whether an object is space debris or active satellite.
    Input: dict with keys matching COLUMNS
    """
    data = pd.DataFrame([orbital_params_dict])[COLUMNS]
    prediction = model.predict(data)[0]

    if prediction == 1:
        return "This object behaves like SPACE DEBRIS"
    else:
        return "This object behaves like ACTIVE SATELLITE"

def predict_with_cleanup(orbital_params_dict):
    """
    Predict object type and generate cleanup plan if debris
    """
    result = predict_object(orbital_params_dict)
    plan = None

    if "DEBRIS" in result:
        ordered_params = [orbital_params_dict[col] for col in COLUMNS]
        plan = generate_cleanup_plan(ordered_params)

    return result, plan
