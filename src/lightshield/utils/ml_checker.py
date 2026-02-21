import os
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "ml_model.pkl")

model = joblib.load(MODEL_PATH)

def check_ml(features):
    return model.predict([features])[0]