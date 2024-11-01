from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from app.db import db

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

@task_bp.post("")
def create_task():
    request_body = request.get_json()
    
    title = request_body["title"]
    description = request_body["description"]
    complete_at = request_body["complete_at"]
    
    new_task = Task(title=title, description=description, complete_at=complete_at)
    db.session.add(new_task)
    db.session.commit()
    
    response = new_task.task_dict()
    return response

@task_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_task(task_id)
    
    return task.task_dict()

@task_bp.get("")
def get_all_tasks():
    query = db.select(Task).order_by(Task.id)
    tasks = db.session.scalars(query)
    
    response_body = [task.task_dict() for task in tasks]
    return response_body
    
def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        response = {"message": f"Task {task_id} is not valid"}
        abort(make_response(response, 400))  
        
    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)
    
    if not task:
        response = {"message": f"Task {task_id} is not found"}
        abort(make_response(response, 404))