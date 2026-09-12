# Cmpe-273-starterlab
# CMPE 273 — Week 1 Lab 1: Your First Distributed System

## Python HTTP Track

This implementation uses two independent Flask processes. Service A listens on port `8080`, and Service B listens on port `8081`.

## Run Locally

Open two terminals from the project directory.

### Terminal 1 — Service A

```bash
cd python-http/service-a
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Terminal 2 — Service B

```bash
cd python-http/service-b
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

For Windows, activate the virtual environment using:

```bash
.venv\Scripts\activate
```

Service A runs on port `8080`, and Service B runs on port `8081`.

## Verify Successful Requests

```bash
curl http://127.0.0.1:8080/health
curl http://127.0.0.1:8081/health
curl "http://127.0.0.1:8081/call-echo?msg=hello"
```

Expected output:

```text
{"status":"ok"}
{"status":"ok"}
{"service_a":{"echo":"hello"},"service_b":"ok"}
```

Example Service A log:

```text
service=A endpoint=/echo status=ok latency_ms=0
```

Example Service B log:

```text
service=B endpoint=/call-echo status=ok latency_ms=4
```

The exact latency may vary depending on the computer.

## Verify Independent Failure

Stop Service A by pressing `Ctrl+C`, but leave Service B running.

Then run:

```bash
curl -i "http://127.0.0.1:8081/call-echo?msg=hello"
```

Expected result:

```text
HTTP/1.1 503 SERVICE UNAVAILABLE
```

Example response:

```json
{
  "error": "HTTPConnectionPool: Failed to establish a new connection",
  "service_a": "unavailable",
  "service_b": "ok"
}
```

The exact connection-error message may vary depending on the operating system.

Example Service B error log:

```text
service=B endpoint=/call-echo status=error error="HTTPConnectionPool(...): Failed to establish a new connection" latency_ms=1
```

Service B handles the failure of Service A by returning a `503 Service Unavailable` response instead of crashing.

## Timeout Handling

Service B uses a one-second timeout when calling Service A. This prevents Service B from waiting indefinitely if Service A is slow or unavailable.

## Request Logging

The services log information about requests, including:

- Service name
- Endpoint
- Request status
- Request latency
- Error details when applicable

## What Makes This Distributed?

The application is distributed because Service A and Service B run as separate processes on separate network ports and communicate through HTTP rather than through a direct function call. Each service can be started, stopped, and observed independently. Therefore, Service B must explicitly handle Service A's network failures, connection errors, and response delays.

## Conclusion

This lab demonstrates:

- Two independent Flask services
- HTTP communication between services
- Separate processes and network ports
- Health-check endpoints
- Request forwarding
- Request logging
- Timeout handling
- Independent service failure handling
