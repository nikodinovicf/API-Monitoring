from prometheus_client import Counter, Histogram, Gauge

class Metrics:
    request_latency = Histogram('flask_api_request_latency_seconds', 'API request latency', ['endpoint'])
    request_counter = Counter('flask_api_requests_total', 'Total API requests', ['method', 'endpoint'])
    request_errors = Counter('flask_api_request_errors', 'API errors', ['method', 'endpoint', 'status_code'])
    response_size = Histogram('flask_api_response_size_bytes', 'Response size in bytes', ['endpoint'])
    health_status = Gauge('flask_api_health_status', 'Application health status (1 = OK, 0 = Error)')
    health_requests = Counter('flask_api_health_requests_total', 'Health check requests')
    active_requests = Gauge('flask_api_active_requests', 'Currently active requests')
    request_duration = Histogram('flask_http_request_duration_seconds', 'Duration of HTTP requests in seconds', ['method', 'endpoint', 'status'])
    api_response_status_total = Counter('flask_api_response_status_total', 'Total API response statuses', ['status_code'])
