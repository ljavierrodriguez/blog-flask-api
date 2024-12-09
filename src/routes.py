import datetime
from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Post

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

@api.route('/posts')
def get_all_posts():

    try:
        posts = Post.query.all()
        posts = [post.serialize() for post in posts]

        return jsonify({ "posts": posts })

    except Exception as e:
        abort(500)


@api.route('/my-posts')
@jwt_required()
def get_all_my_posts():

    try:
        id = get_jwt_identity()
        posts = Post.query.filter(Post.user_id == id).all()
        posts = [post.serialize() for post in posts]

        return jsonify({ "posts": posts })

    except Exception as e:
        abort(500)

@api.route('/add-post', methods=['POST'])
@jwt_required()
def create_post():
    try:
        id = get_jwt_identity()

        title = request.json.get("title")
        resume = request.json.get("resume", "")
        content = request.json.get("content")

        if not title:
            return jsonify({ "error": "Field (title) is requred"}), 400
        if not content:
            return jsonify({ "error": "Field (content) is requred"}), 400
        
        post = Post()
        post.title = title
        post.resume = resume
        post.content = content
        post.user_id = id

        post.save()

        if post:
            return jsonify(post.serialize()), 201
        
        return jsonify({"error": "Please try again, post not created"}), 400

    except Exception as e:
        abort(500)

@api.route('/posts/<int:post_id>/delete', methods=["DELETE"])
@jwt_required()
def delete_post_by_id(post_id):
    try:
        id = get_jwt_identity()
        post = Post.query.filter(Post.id==post_id, Post.user_id==id).first() 

        if not post:
            return jsonify({ "error": "Post not found"}), 404
        
        post.delete()

        return jsonify({ "success": "Post deleted"}), 200

    except Exception as e:
        abort(500)
