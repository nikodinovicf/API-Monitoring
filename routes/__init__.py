from flask import Blueprint
from flask_restful import Api
from app.resources import Users, User
from app.health_check import HealthCheck

routes_bp = Blueprint('routes', __name__, url_prefix="/api")

# Health check route
@routes_bp.route('/healthz')
def healthz():
    return HealthCheck.check_health()

# Register API resources properly
api = Api(routes_bp)
api.add_resource(Users, '/user')
api.add_resource(User, '/user/<int:id>')
