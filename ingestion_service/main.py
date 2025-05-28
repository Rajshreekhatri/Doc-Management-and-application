import os
from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from models import db
from routes.ingestion import ingest_ns

load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.before_first_request
def create_tables():
    db.create_all()
    
jwt = JWTManager(app)
db.init_app(app)





api = Api(app,prefix="/api/v1", version='1.0')

api.add_namespace(ingest_ns)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
