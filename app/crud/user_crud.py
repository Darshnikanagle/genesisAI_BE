from app.db.models.user_model import User


def create_user(session, user):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_user_by_email(session, email):
    return session.query(User).filter_by(email=email).first()

def get_user_by_id(session, user_id):
    return session.query(User).filter_by(id=user_id).first()

def update_user(session, user_id, **kwargs):
    user = get_user_by_id(session, user_id)
    if not user:
        return None
    for key, value in kwargs.items():
        setattr(user, key, value)
    session.commit()
    return user

def delete_user(session, user_id):
    user = get_user_by_id(session, user_id)
    if user:
        session.delete(user)
        session.commit()
