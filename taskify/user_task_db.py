from flask import Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from flask_marshmallow import Marshmallow
from app import db, ma
import os

user_task_bp = Blueprint('user_task_db', __name__)

# database models
users_tasks = db.Table(
    "users_tasks",
    Column("user_id", db.ForeignKey("user.id"), primary_key=True),
    Column("task_id", db.ForeignKey("task.id"), primary_key=True),
)

class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)          
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    tasks = db.relationship('Task',secondary=users_tasks, backref=db.backref('users', lazy='dynamic'))
    
# attaching Tasks to many users - "Role based app"
class Task(db.Model):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    # task_type = Column(String)
    # task_deadline = Column(Float)
    # time_frame = Column(Float)
    #create_time = Column(DateTime)
    

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','first_name','last_name','email','password','tasks')
        

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id','name','description')
        

user_schema = UserSchema()
users_schema = UserSchema(many=True)

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)