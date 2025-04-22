from app.db.models.thread_message_model import ThreadMessage


def create_thread_message(session, thread_id, user_message, system_message):
    message = ThreadMessage(thread_id=thread_id, user_message=user_message, system_message=system_message)
    session.add(message)
    session.commit()
    return message

def get_thread_message_by_id(session, message_id):
    return session.query(ThreadMessage).filter_by(id=message_id).first()

def update_thread_message(session, message_id, **kwargs):
    message = get_thread_message_by_id(session, message_id)
    if not message:
        return None
    for key, value in kwargs.items():
        setattr(message, key, value)
    session.commit()
    return message

def delete_thread_message(session, message_id):
    message = get_thread_message_by_id(session, message_id)
    if message:
        session.delete(message)
        session.commit()
