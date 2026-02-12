from flask import Flask
from src.lightshield.utils.signature_checker import check_signature

app = Flask(__name__)

@app.route("/")
def home():
    return "LightShield is Running 🚀"


@app.route("/test/<path:payload>")
def test(payload):
    result = check_signature(payload)
    return f"Result: {result}"


if __name__ == "__main__":
    app.run(debug=True)
