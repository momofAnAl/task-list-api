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