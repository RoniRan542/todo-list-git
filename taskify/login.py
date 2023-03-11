from flask import Blueprint, jsonify, request, render_template
from flask_jwt_extended import create_access_token
from user_task_db import User


login_bp = Blueprint('login', __name__)

@login_bp.route('/login-page')
def login_page():
    return render_template('login.html')
    
@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    print("inside backend side")
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']
    # check if user exists in the db
    user = User.query.filter_by(email=email, password=password).first()
    if user:
        access_token = create_access_token(identity=email)
        return jsonify(message="login success",access_token=access_token, id=user.id, name=user.first_name)
    else:
        return jsonify(message="Bad email or password")
