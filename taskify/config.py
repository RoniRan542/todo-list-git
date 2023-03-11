
from flask import Blueprint
from app import db
from user_task_db import User, Task

config_bp = Blueprint('config',__name__)

# create database
@config_bp.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created!')

# destroy database
@config_bp.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('database drop')

# database seeding
@config_bp.cli.command('db_seed')
def db_seed():
    test_user = User(first_name = 'Roni',
                     last_name='Cohen',
                     email='test@test.com',
                     password='password'
                     )
    db.session.add(test_user)
    
    test_task = Task(name='Programming',
                     description='demo: developing an online game',
                     )
    db.session.add(test_task)
    db.session.commit()
    print('database seeded')

