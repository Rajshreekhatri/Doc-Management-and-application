from flask import Flask
from flask_restx import Api
from dotenv import load_dotenv
import os
from models import db
from routes.users import user_ns

load_dotenv()

app = Flask(__name__)

user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
host = os.getenv('POSTGRES_HOST')
port = os.getenv('POSTGRES_PORT')
db_name = os.getenv('POSTGRES_DB')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.before_first_request
def create_tables():
    db.create_all()

db.init_app(app)
jwt = JWTManager(app)



api = Api(app,prefix="/api/v1", version='1.0')
api.add_namespace(user_ns)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
