from flask import request
from models import User, db
from flask_restx import Namespace, Resource, abort
from flask_jwt_extended import jwt_required, get_jwt

user_ns = Namespace('users')

def role_required(allowed_roles):
    def wrapper(fn):
        @jwt_required()
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims.get('role') not in allowed_roles:
                abort(403, 'Insufficient permissions')
            return fn(*args, **kwargs)
        return decorator
    return wrapper
    
@user_ns.route('/')
class UserList(Resource):
    @jwt_required()
    @role_required(['admin'])
    def get(self):
        users = User.query.all()
        return [{'id': u.id, 'username': u.username, 'role': u.role} for u in users]

@user_ns.route('/<int:id>/role')
class UserRole(Resource):
    @jwt_required()
    @role_required(['admin'])
    def patch(self, id):
        data = request.json
        user = User.query.get(id)
        if not user:
            return {'msg': 'User not found'}, 404
        user.role = data.get('role', user.role)
        db.session.commit()
        return {'msg': f'Role for user {id} updated to {user.role}'}
