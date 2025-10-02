from sqlalchemy.orm import Session
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")))

from server.rtcrm.database.models import User, Session as Sess, Query, PlanResponse
import uuid

def create_session(db: Session, user_external_id: str | None) -> Sess:
    user = None
    if user_external_id:
        user = db.query(User).filter(User.external_id == user_external_id).first()
        if not user:
            user = User(external_id=user_external_id)
            db.add(user); db.flush()
    sess = Sess(user_id=user.id if user else None)
    db.add(sess); db.flush()
    return sess

def log_query(db: Session, session_id: uuid.UUID, goal: str) -> Query:
    q = Query(session_id=session_id, goal=goal)
    db.add(q); db.flush()
    return q

def save_plan(db: Session, query_id: uuid.UUID, answers: dict, provider: str) -> PlanResponse:
    pr = PlanResponse(query_id=query_id, answers=answers, model_provider=provider)
    db.add(pr); db.flush()
    return pr