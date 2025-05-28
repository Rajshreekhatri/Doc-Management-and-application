from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import create_access_token
from models import User, db
from werkzeug.security import generate_password_hash, check_password_hash

auth_ns = Namespace('auth')

user_model = auth_ns.model('User', {
    'username': fields.String(required=True),
    'password': fields.String(required=True),
    'role': fields.String(enum=['admin', 'editor', 'viewer'], required=True)
})

@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(user_model)
    def post(self):
        data = request.json
        username = data['username']
        password = data['password']
        role = data['role']

        if User.query.filter_by(username=username).first():
            return {'msg': 'User already exists'}, 400

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        return {'msg': 'User registered'}, 201

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(user_model)
    def post(self):
        data = request.json
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return {'msg': 'Invalid credentials'}, 401

        access_token = create_access_token(identity=user.username, additional_claims={'role': user.role})
        return {'access_token': access_token}


@auth_ns.route('/token')
class TokenInfo(Resource):
    @jwt_required()
    def get(self):
        identity = get_jwt_identity()
        return {
            'message': 'Token is valid',
            'user': identity
        }, 200

@auth_ns.route('/me')
class CurrentUser(Resource):
    @jwt_required()
    @auth_ns.response(200, 'User data retrieved')
    @auth_ns.response(404, 'User not found')
    def get(self):
        """
        Get the current authenticated user's full data from the database.
        """
        identity = get_jwt_identity()
        user = User.query.filter_by(username=identity['username']).first()
        if not user:
            return {'message': 'User not found'}, 404

        return {
            'id': user.id,
            'username': user.username,
            'role': user.role
        }, 200