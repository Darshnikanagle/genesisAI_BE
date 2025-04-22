from app.db.models.thread_model import Thread

def create_thread(session, thread_type, user_id):
    thread = Thread(type=thread_type, user_id=user_id)
    session.add(thread)
    session.commit()
    return thread

def get_thread_by_id(session, thread_id):
    return session.query(Thread).filter_by(id=thread_id).first()

def update_thread(session, thread_id, **kwargs):
    thread = get_thread_by_id(session, thread_id)
    if not thread:
        return None
    for key, value in kwargs.items():
        setattr(thread, key, value)
    session.commit()
    return thread

def delete_thread(session, thread_id):
    thread = get_thread_by_id(session, thread_id)
    if thread:
        session.delete(thread)
        session.commit()
