from flask import Blueprint, jsonify, request, render_template
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from user_task_db import User, Task, task_schema, tasks_schema
from app import db
crud_bp = Blueprint('crud', __name__)


@crud_bp.route('/add_task/<int:user_id>', methods=['POST'])
@jwt_required() # force the user to login in order to get a jwt token
def add_task(user_id:int):
    user = User.query.filter_by(id=user_id).first()
    if user:
        if request.is_json:
            task_name=request.json['name']
            task_description=request.json['description']
        else:
            task_name=request.form['name']
            task_description=request.form['description']
        new_task = Task(name=task_name, description=task_description)
        user.tasks.append(new_task)
        db.session.commit()
        result = []
        for task in tasks_schema.dump(user.tasks):
            result.append(task)
        return render_template('user_todo.html', tasks=result)
    else:
        return jsonify(message="There is already a task with that name"), 409
        


@crud_bp.route('/edit_task/<int:user_id>', methods=['POST','PUT'])
@jwt_required() # force the user to login in order to get a jwt token
def edit_task(user_id:int):
    user = User.query.filter_by(id=user_id).first()
    if user:
        task_id = int(request.args.get('task_id'))
        task = Task.query.filter_by(id=task_id).first()
        task.name = request.json['name']
        task.description = request.json['description']
        db.session.commit()
        return jsonify(message="Task updated"),202
    else:
        return jsonify(message="Failed to update"),404



@crud_bp.route('/delete_task/<int:user_id>', methods=['DELETE'])
@jwt_required() # force the user to login in order to get a jwt token
def delete_task(user_id:int):
    user = User.query.filter_by(id=user_id).first()
    if user:
        task_id = int(request.args.get('task_id'))
        print(task_id)
        task = Task.query.filter_by(id=task_id).first()
        db.session.delete(task)
        db.session.commit()
        result = []
        for task in tasks_schema.dump(user.tasks):
            result.append(task)
        return render_template('user_todo.html', tasks=result)
    else:
        return jsonify(message="Delition failed")
    


@crud_bp.route('/tasks', methods=['GET'])
def tasks():
    task_list = Task.query.all()
    result = tasks_schema.dump(task_list) 
    return jsonify(result)

@crud_bp.route('/todo_list/<int:user_id>', methods=['GET'])
def todo_list(user_id: int):
    user = User.query.filter_by(id=user_id).first()
    
    if user:
        result = []
        for task in tasks_schema.dump(user.tasks):
            result.append(task)
        return render_template('user_todo.html', tasks=result)
    return jsonify(message="No existing todo-list found"),404
 
