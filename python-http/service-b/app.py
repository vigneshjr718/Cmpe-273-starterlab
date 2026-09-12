import logging
import os
import time

import requests
from flask import Flask, request, jsonify

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
app = Flask(__name__)

SERVICE_A = os.environ.get("SERVICE_A_URL", "http://127.0.0.1:8080")
REQUEST_TIMEOUT_SECONDS = 1.0


def log_request(endpoint, status, started_at):
    latency_ms = int((time.perf_counter() - started_at) * 1000)
    logging.info(
        "service=B endpoint=%s status=%s latency_ms=%s",
        endpoint,
        status,
        latency_ms,
    )

@app.get("/health")
def health():
    started_at = time.perf_counter()
    response = jsonify(status="ok")
    log_request("/health", 200, started_at)
    return response

@app.get("/call-echo")
def call_echo():
    started_at = time.perf_counter()
    msg = request.args.get("msg", "")
    try:
        r = requests.get(
            f"{SERVICE_A}/echo",
            params={"msg": msg},
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        r.raise_for_status()
        data = r.json()
        log_request("/call-echo", 200, started_at)
        return jsonify(service_b="ok", service_a=data)
    except requests.RequestException as error:
        logging.error("service=B dependency=service-A error=%s", error)
        log_request("/call-echo", 503, started_at)
        return jsonify(service_b="ok", service_a="unavailable", error=str(error)), 503

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8081)
