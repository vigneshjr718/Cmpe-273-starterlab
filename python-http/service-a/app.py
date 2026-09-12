import logging
import time

from flask import Flask, g, jsonify, request

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
app = Flask(__name__)


@app.before_request
def start_timer():
    g.request_started_at = time.perf_counter()


@app.after_request
def log_request(response):
    started_at = getattr(g, "request_started_at", time.perf_counter())
    latency_ms = int((time.perf_counter() - started_at) * 1000)
    logging.info(
        "service=A endpoint=%s status=%s latency_ms=%s",
        request.path,
        response.status_code,
        latency_ms,
    )
    return response


@app.get("/health")
def health():
    return jsonify(status="ok")

@app.get("/echo")
def echo():
    msg = request.args.get("msg", "")
    return jsonify(echo=msg)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
