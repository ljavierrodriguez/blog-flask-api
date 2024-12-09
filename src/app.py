import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db
from dotenv import load_dotenv
from routes import api

load_dotenv()

PATH = os.path.abspath('instance')

app = Flask(__name__, instance_path=PATH)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICACIONES'] = False 
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL') 
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY') 

db.init_app(app)
Migrate(app, db)
jwt = JWTManager(app)
CORS(app)

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({ "error": "page not found"}), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({ "error": "internal server error"}), 500

app.register_blueprint(api, url_prefix="/api")

if __name__ == '__main__':
    app.run()