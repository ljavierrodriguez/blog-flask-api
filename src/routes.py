import datetime
from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from models import User

api = Blueprint("api", __name__)

@api.route('/login', methods=['POST'])
def login():
    try:
        username = request.json.get('username')
        password = request.json.get('password')

        if not username:
            return jsonify({ "error": "Field (username) is requred"}), 400
        if not password:
            return jsonify({ "error": "Field (password) is requred"}), 400
        
        user = User.query.filter_by(username=username).first()

        if not user:
            return jsonify({ "error": "Username/Password are incorrects, please try again"}), 401
        
        if not check_password_hash(user.password, password):
            return jsonify({ "error": "Username/Password are incorrects, please try again"}), 401
        
        expire = datetime.timedelta(days=3)
        access_token = create_access_token(identity=str(user.id), expires_delta=expire)

        return jsonify({ "acceses_token": access_token}), 200

    except Exception as e:
        abort(500)

@api.route('/register', methods=['POST'])
def register():
    try:

        username = request.json.get('username')
        password = request.json.get('password')

        if not username:
            return jsonify({ "error": "this field (username) is requred"}), 400
        if not password:
            return jsonify({ "error": "this field (username) is requred"}), 400
        
        found = User.query.filter_by(username=username).first()

        if found:
            return jsonify({ "error": "this field (username) already taken"}), 400
        
        user = User()
        user.username = username
        user.password = generate_password_hash(password)
        user.save()
        
        expire = datetime.timedelta(days=3)
        access_token = create_access_token(identity=str(user.id), expires_delta=expire)

        return jsonify({ "acceses_token": access_token}), 200
    
    except Exception as e:
        abort(500)

    