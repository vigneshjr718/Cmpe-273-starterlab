# Python HTTP Track — Week 1 Lab 1

This implementation uses two independent Flask processes. Service A listens on
port 8080 and Service B listens on port 8081.

## Run locally

Open two terminals from the `python-http` directory.

### Terminal 1 — Service A (port 8080)

```bash
cd service-a
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Terminal 2 — Service B (port 8081)

```bash
cd service-b
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Verify success

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

Service A logs its request, for example:

```text
service=A endpoint=/echo status=200 latency_ms=0
```

Service B logs its completed request, for example:

```text
service=B endpoint=/call-echo status=200 latency_ms=4
```

## Verify independent failure

Stop Service A with `Ctrl+C` but leave Service B running, then repeat:

```bash
curl -i "http://127.0.0.1:8081/call-echo?msg=hello"
```

Expected result (the exact connection-error text can vary by operating system):

```text
HTTP/1.1 503 SERVICE UNAVAILABLE
...
{"error":"...Connection refused...","service_a":"unavailable","service_b":"ok"}
```

Service B records both the dependency error and the 503 response in its log:

```text
service=B dependency=service-A error=HTTPConnectionPool(...): Failed to establish a new connection
service=B endpoint=/call-echo status=503 latency_ms=1
```

Service B uses a one-second `requests` timeout for its call to Service A. You
can point it at another Service A address with `SERVICE_A_URL`, for example:
`SERVICE_A_URL=http://127.0.0.1:8080 python app.py`.

## What makes this distributed?

The application is distributed because Service A and Service B run as separate
processes with separate network ports and communicate through an HTTP request,
rather than a direct function call. Each service can be started, stopped, and
observed independently, so Service B must handle Service A's network failures
and response delay explicitly.
