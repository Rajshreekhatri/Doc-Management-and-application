
from flask_restx import Namespace, Resource, abort
from flask import request
from flask_jwt_extended import jwt_required, get_jwt
import uuid
from models import IngestionJob, db

ingest_ns = Namespace('ingestion')

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

@ingest_ns.route('/trigger')
class IngestTrigger(Resource):
    @role_required(['admin', 'editor'])
    def post(self):
        job_id = str(uuid.uuid4())
        new_job = IngestionJob(job_id=job_id, status='started')
        db.session.add(new_job)
        db.session.commit()
        return {'msg': 'Ingestion triggered', 'job_id': job_id}

@ingest_ns.route('/status/<string:job_id>')
class IngestStatus(Resource):
    @jwt_required()
    def get(self, job_id):
        job = IngestionJob.query.filter_by(job_id=job_id).first()
        if not job:
            return {'msg': 'Job not found'}, 404
        return {'job_id': job.job_id, 'status': job.status}

@ingest_ns.route('/jobs')
class IngestJobs(Resource):
    @jwt_required()
    def get(self):
        jobs = IngestionJob.query.all()
        return [{'job_id': j.job_id, 'status': j.status} for j in jobs]
