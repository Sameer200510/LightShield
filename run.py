import datetime
import requests
import os
from flask import Flask, render_template, request, Response
from src.lightshield.utils.signature_checker import check_signature
from src.lightshield.utils.preprocessor import extract_features
from src.lightshield.utils.ml_checker import check_ml

app = Flask(__name__)

TARGET_SERVER = "http://httpbin.org"

# ----------------------
# Global State
# ----------------------
total_requests = 0
total_threats = 0
ml_count = 0
sig_count = 0

ip_request_count = {}
ip_blocked = {}

recent_requests = []


# ----------------------
# Dashboard Route
# ----------------------
@app.route("/", methods=["GET", "POST"])
def home():
    global total_requests, total_threats, ml_count, sig_count, recent_requests

    result = None
    detection_type = None

    if request.method == "POST":
        payload = request.form["payload"]
        total_requests += 1

        sig_result = check_signature(payload)
        features = extract_features(payload)
        ml_result = check_ml(features)

        if sig_result == 1:
            result = "🚨 Malicious Request Detected"
            detection_type = "Signature-Based Detection"
            total_threats += 1
            sig_count += 1

        elif ml_result == 1:
            result = "🚨 Malicious Request Detected"
            detection_type = "ML-Based Detection"
            total_threats += 1
            ml_count += 1

        else:
            result = "✅ Safe Request"
            detection_type = "No Threat Detected"

        # Logging
        if result.startswith("🚨"):
            with open("logs/detections.log", "a") as log:
                log.write(
                    f"{datetime.datetime.now()} | {detection_type} | {payload}\n"
                )

        # Live feed
        event = {
            "time": datetime.datetime.now().strftime("%H:%M:%S"),
            "payload": payload[:60],
            "status": "Threat" if result.startswith("🚨") else "Safe"
        }

        recent_requests.insert(0, event)
        recent_requests[:] = recent_requests[:20]

    return render_template(
        "index.html",
        result=result,
        detection_type=detection_type,
        total_requests=total_requests,
        total_threats=total_threats,
        ml_count=ml_count,
        sig_count=sig_count,
        recent_requests=recent_requests
    )


# ----------------------
# API Mode
# ----------------------
@app.route("/api/check", methods=["POST"])
def api_check():
    data = request.json
    payload = data.get("payload", "")

    sig_result = check_signature(payload)
    features = extract_features(payload)
    ml_result = check_ml(features)

    if sig_result == 1:
        return {"status": "blocked", "source": "signature"}
    elif ml_result == 1:
        return {"status": "blocked", "source": "ml"}
    else:
        return {"status": "allowed"}


# ----------------------
# Reverse Proxy Mode
# ----------------------
@app.route("/proxy/<path:path>", methods=["GET", "POST"])
def proxy(path):
    global ip_request_count, ip_blocked

    client_ip = request.remote_addr

    # Agar IP pehle hi block hai
    if client_ip in ip_blocked:
        return Response("🚨 LightShield Ne Aapki IP Block Kar Di Hai 😎", status=403)

    # Count requests
    ip_request_count[client_ip] = ip_request_count.get(client_ip, 0) + 1

    # Rate limit exceed
    if ip_request_count[client_ip] > 100:
        ip_blocked[client_ip] = True
        return Response("🚨 Rate Limit Exceed Hogayi Aur IP Bhi Block Ho Gayi 😭😭", status=403)

    # Extract payload
    payload = request.get_data(as_text=True) or request.query_string.decode()

    sig_result = check_signature(payload)
    features = extract_features(payload)
    ml_result = check_ml(features)

    # Malicious block
    if sig_result == 1 or ml_result == 1:
        ip_blocked[client_ip] = True
        return Response("🚨 Kuch Gadbad Hai... Isliye LightShield Ne Block Kar Diya 😏", status=403)

    # Safe request forward karo
    url = f"{TARGET_SERVER}/{path}"

    if request.method == "POST":
        resp = requests.post(url, data=request.form)
    else:
        resp = requests.get(url, params=request.args)

    return Response(resp.content, resp.status_code)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)