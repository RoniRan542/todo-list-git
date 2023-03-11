from flask import Blueprint, jsonify, request, render_template
from app import db
from flask_sqlalchemy import SQLAlchemy
from user_task_db import User

register_bp = Blueprint('register', __name__)

@register_bp.route('/register-page')
def register_page():
    return render_template('register.html')

@register_bp.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    test_if_email_exists = User.query.filter_by(email=email).first()
    if test_if_email_exists:
        return jsonify(message='This email already exists')
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return render_template("register_success.html", user_name= request.form['first_name']),201
