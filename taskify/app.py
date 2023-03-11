from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_mail import Mail

import json
import os.path

app = Flask(__name__)
# sqlite database configuration. Crucial to set before using SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'taskify.db')
# jwt config secret key
app.config['JWT_SECRET_KEY'] = 'super-secret-change-it-later' # change this later

# app variables
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
mail = Mail(app)

from register import register_bp
from login import login_bp
from mailing import mail_bp
from crud import crud_bp
from user_task_db import user_task_bp
from config import config_bp


app.register_blueprint(user_task_bp)
app.register_blueprint(register_bp)
app.register_blueprint(login_bp)
app.register_blueprint(mail_bp)
app.register_blueprint(crud_bp)
app.register_blueprint(config_bp)


# set environment variables. Later put it outside of files
os.environ['MAIL_USERNAME'] = 'cc5aee2e6e7071'
os.environ['MAIL_PASSWORD'] = '2dd92cb0c86da0'

# config mail server
app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

# basic routing

@app.route('/')
def home():
    return render_template('index.html', version='1.0.0')
    

@app.route('/about')
def about():
    return render_template('about.html', version='1.0.0')



@app.route('/not_found')
def not_found():
    return jsonify(message='That resource was not found'),404
