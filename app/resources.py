from flask_restful import Resource, reqparse, marshal_with, abort, fields
from app.models import UserModel, db

user_args = reqparse.RequestParser()
user_args.add_argument('username', type=str, required=True, help="Username is required")
user_args.add_argument('email', type=str, required=True, help="Email is required")

user_fields = {'id': fields.Integer, 'username': fields.String, 'email': fields.String}

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
        return user, 201

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
