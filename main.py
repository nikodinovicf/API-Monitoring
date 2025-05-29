from app import app
from app.middleware import RequestTracker
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from flask import Response

@app.before_request
def before_request():
    RequestTracker.before_request()

@app.after_request
def after_request(response):
    return RequestTracker.after_request(response)

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), content_type=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
