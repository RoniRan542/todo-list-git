from flask import Blueprint, jsonify, request
from flask_mail import Mail, Message
from app import mail
from user_task_db import User

mail_bp = Blueprint('mail', __name__)

@mail_bp.route('/retrieve_password/<string:email>', methods=['GET'])
def retrieve_password(email:str):
    user = User.query.filter_by(email=email).first()
    if user:
        msg = Message("your taskify password is " + user.password,
                      sender="admin@taskify.com",
                      recipients=[email])
        mail.send(msg)
        return jsonify(message="Password was sent to " + email)
    else:
        return jsonify(message="This email doesn't exist"),401