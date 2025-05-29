from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client import Gauge
from sqlalchemy import text
import os
from time import time

# Initialize Flask app & database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

db = SQLAlchemy(app)  # Initialize SQLAlchemy with Flask app
api = Api(app)  # Initialize Flask-RESTful API

# Ensure database exists
with app.app_context():
    db.create_all()

# Define Prometheus Metrics for monitoring API performance
request_latency = Histogram('flask_api_request_latency_seconds', 'API request latency', ['endpoint'])
request_counter = Counter('flask_api_requests_total', 'Total API requests', ['method', 'endpoint'])
request_api_calls = Counter('flask_api_calls_total', 'Total API calls', ['method', 'endpoint'])
request_errors = Counter('flask_api_request_errors', 'API errors', ['method', 'endpoint', 'status_code'])
response_size = Histogram('flask_api_response_size_bytes', 'Response size in bytes', ['endpoint'])
health_status = Gauge('flask_api_health_status', 'Application health status (1 = OK, 0 = Error)')
health_requests = Counter('flask_api_health_requests_total', 'Health check requests')
active_requests = Gauge('flask_api_active_requests', 'Currently active requests')
request_duration = Histogram('flask_http_request_duration_seconds', 'Duration of HTTP requests in seconds', ['method', 'endpoint', 'status'])
api_response_status_total = Counter('flask_api_response_status_total', 'Total API response statuses', ['status_code'])
#http_requests_errors_total = Counter('flask_http_requests_errors_total', 'Total HTTP request errors', ['method', 'endpoint', 'status_code'])
#process_resident_memory_bytes = Gauge('flask_process_resident_memory_bytes', 'Resident memory size of the process in bytes')
#http_request_size_bytes = Histogram('flask_http_request_size_bytes', 'Size of HTTP requests in bytes', ['method', 'endpoint'])
#http_response_size_bytes = Histogram('flask_http_response_size_bytes', 'Size of HTTP responses in bytes', ['method', 'endpoint'])
#process_open_fds = Gauge('flask_process_open_fds', 'Number of open file descriptors in the process')
#uptime_seconds = Gauge('flask_uptime_seconds', 'Application uptime in seconds')


# Health check endpoint
@app.route('/healthz')
def healthz():
    health_requests.inc()  # Increment health check request counter
    db_file_exists = os.path.exists("database.db")

    try:
        db.session.execute(text('SELECT 1'))  # Check if database is reachable
        health_status.set(1) 
        return {"status": "ok", "database": "connected", "db_file": db_file_exists}, 200
    except Exception as e:
        health_status.set(0)
        return {"status": "error", "database": "unavailable", "db_file": db_file_exists, "details": str(e)}, 500

# Middleware to track request start time and increment counters
@app.before_request
def before_request():
    request.start_time = time()
    request_counter.labels(method=request.method, endpoint=request.path).inc()
    active_requests.inc()  # Track active requests

# Middleware to track request duration and response details
@app.after_request
def after_request(response):
    latency = time() - request.start_time
    request_latency.labels(endpoint=request.path).observe(latency)
    response_size.labels(endpoint=request.path).observe(len(response.data))

    api_response_status_total.labels(status_code=response.status_code).inc()  # Track API response statuses

    if response.status_code >= 400:
        request_errors.labels(method=request.method, endpoint=request.path, status_code=response.status_code).inc()

    active_requests.dec()  # Decrement active requests counter

    # Track HTTP request duration
    request_duration.labels(
        method=request.method,
        endpoint=request.path,
        status=response.status_code
    ).observe(latency)

    return response

# Define database model
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# Request parser for user data validation
user_args = reqparse.RequestParser()
user_args.add_argument('username', type=str, required=True, help='Username is required')
user_args.add_argument('email', type=str, required=True, help='Email is required')

# Response fields for formatting output data
user_fields = {'id': fields.Integer, 'username': fields.String, 'email': fields.String}

# Resource for retrieving all users or creating a new user
class Users(Resource):
    @marshal_with(user_fields)
    def get(self):
        users = UserModel.query.all()
        return users if users else abort(404, message="No users found")

    @marshal_with(user_fields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(username=args['username'], email=args['email'])
        db.session.add(user)
        db.session.commit()
        return user, 201  # Return created user with HTTP 201

# Resource for retrieving, updating, or deleting a single user
class User(Resource):
    @marshal_with(user_fields)
    def get(self, id):
        return UserModel.query.get_or_404(id)

    @marshal_with(user_fields)
    def put(self, id):
        args = user_args.parse_args()
        user = UserModel.query.get_or_404(id)
        user.username = args['username']
        user.email = args['email']
        db.session.commit()
        return user

    def delete(self, id):
        user = UserModel.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, 204

# Endpoint for Prometheus metrics
@app.route('/metrics')
def metrics():
    return Response(generate_latest(), content_type=CONTENT_TYPE_LATEST)


# Register API routes
api.add_resource(Users, '/api/user')
api.add_resource(User, '/api/user/<int:id>')

# Home route for basic interaction
@app.route('/')
def home():
    return "<h1>Welcome to the presentation of Prometheus monitoring tool!</h1>"

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
