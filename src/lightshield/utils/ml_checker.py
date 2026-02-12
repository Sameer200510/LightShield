import joblib

model = joblib.load("src/lightshield/models/ml_model.pkl")

def check_ml(features):
    return model.predict([features])[0]
