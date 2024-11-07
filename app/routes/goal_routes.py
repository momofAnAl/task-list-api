from flask import Blueprint, abort, make_response, request
from app.models.goal import Goal
from app.db import db

bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()
    
    if "title" not in request_body:
        response_body = {"details": "Invalid data"}
        return make_response(response_body, 400)
    
    title = request_body["title"]
    new_goal = Goal(title=title)
    db.session.add(new_goal)
    db.session.commit()
    
    response_body = {"goal": new_goal.goal_dict()}
    return response_body, 201

@bp.get("")
def get_all_saved_goals():
    query = db.select(Goal).order_by(Goal.id)
    goals = db.session.scalars(query)
    
    response_body = [goal.goal_dict() for goal in goals]
    return response_body

@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)
    
    db.session.add(goal)
    db.session.commit()

    response_body = {"goal": goal.goal_dict()}
    return response_body

@bp.put("/<goal_id>")
def update_one_goal(goal_id):
    goal= validate_goal(goal_id)
    
    request_body = request.get_json()
    goal.title = request_body["title"]
    
    # db.session.add(title)
    db.session.commit()
    
    response_body = {"goal": goal.goal_dict()}
    return make_response(response_body, 200)

@bp.delete("/<goal_id>")
def delete_one_goal(goal_id):
    goal = validate_goal(goal_id)
    
    db.session.delete(goal)
    db.session.commit()
    
    response = {"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}
    return make_response(response, 200)
    
    
def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        response = {"message": f"Goal {goal_id} is invalid" }
        abort(make_response(response, 400))
        
    query = db.select(Goal).where(Goal.id == goal_id)
    goal = db.session.scalar(query)
    
    if not goal:
        response = {"message": f"Goal {goal_id} is not found"}
        abort(make_response(response, 404))
    
    return goal