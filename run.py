from flask import Flask
from src.lightshield.utils.signature_checker import check_signature
from src.lightshield.utils.preprocessor import extract_features
from src.lightshield.utils.ml_checker import check_ml

app = Flask(__name__)
@app.route("/")
def home():
    return "LightShield is Running 🚀"

@app.route("/test/<path:payload>")
def test(payload):

    # Signature Layer
    sig_result = check_signature(payload)

    # ML Layer
    features = extract_features(payload)
    ml_result = check_ml(features)

    # Hybrid Decision
    if sig_result == 1 or ml_result == 1:
        final_result = "🚨 Malicious Request Detected"
    else:
        final_result = "✅ Safe Request"

    return final_result
if __name__ == "__main__":
    app.run(debug=True)
