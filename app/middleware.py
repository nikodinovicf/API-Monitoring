from flask import request
from time import time
from app.metrics import Metrics

class RequestTracker:
    @staticmethod
    def before_request():
        request.start_time = time()
        Metrics.request_counter.labels(method=request.method, endpoint=request.path).inc()
        Metrics.active_requests.inc()  # Track active requests

    @staticmethod
    def after_request(response):
        latency = time() - request.start_time
        Metrics.request_latency.labels(endpoint=request.path).observe(latency)
        Metrics.response_size.labels(endpoint=request.path).observe(len(response.data))

        Metrics.api_response_status_total.labels(status_code=response.status_code).inc()  # Track API response statuses

        if response.status_code >= 400:
            Metrics.request_errors.labels(method=request.method, endpoint=request.path, status_code=response.status_code).inc()

        Metrics.active_requests.dec()  # Decrement active requests counter

        Metrics.request_duration.labels(
            method=request.method,
            endpoint=request.path,
            status=response.status_code
        ).observe(latency)

        return response
