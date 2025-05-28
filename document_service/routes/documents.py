from flask_restx import Namespace, Resource, fields
from flask import request
from models import Document, db
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_restx import abort


doc_ns = Namespace('documents')

document_model = doc_ns.model('Document', {
    'title': fields.String(required=True),
    'content': fields.String
})

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

@doc_ns.route('/')
class DocumentList(Resource):
    @doc_ns.expect(document_model)
    @role_required(['admin', 'editor'])
    def post(self):
        data = request.json
        new_doc = Document(title=data['title'], content=data.get('content'))
        db.session.add(new_doc)
        db.session.commit()
        return {'msg': 'Document created', 'id': new_doc.id}, 201

    @jwt_required()
    def get(self):
        docs = Document.query.all()
        return [{'id': d.id, 'title': d.title, 'content': d.content} for d in docs]

@doc_ns.route('/<int:id>')
class Document(Resource):
    @jwt_required()
    def get(self, id):
        doc = Document.query.get(id)
        if not doc:
            return {'msg': 'Document not found'}, 404
        return {'id': doc.id, 'title': doc.title, 'content': doc.content}

    @doc_ns.expect(document_model)
    @role_required(['admin', 'editor'])
    def put(self, id):
        doc = Document.query.get(id)
        if not doc:
            return {'msg': 'Document not found'}, 404
        data = request.json
        doc.title = data['title']
        doc.content = data.get('content')
        db.session.commit()
        return {'msg': f'Document {id} updated'}

    @role_required(['admin'])
    def delete(self, id):
        doc = Document.query.get(id)
        if not doc:
            return {'msg': 'Document not found'}, 404
        db.session.delete(doc)
        db.session.commit()
        return {'msg': f'Document {id} deleted'}
