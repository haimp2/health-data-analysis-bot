from data.database import DataBase
from data.models import User


def add_user(chat_id, user_state, user_first_choice):
    session = DataBase.get_session()
    user = session.query(User).filter_by(chat_id=chat_id).first()
    
    if user:
        user.user_state = user_state
        user.user_first_choice = user_first_choice
    else:
        session.add(User(chat_id=chat_id, user_state=user_state, user_first_choice=user_first_choice))

    session.commit()
    session.close()


def update_user(chat_id, **kwargs):
    session = DataBase.get_session()
    user = session.query(User).filter_by(chat_id=chat_id).first()
    
    if user:
        for key, value in kwargs.items():
            setattr(user, key, value)
        session.commit()
    
    user_dict = {column.name: getattr(user, column.name) for column in user.__table__.columns}
    session.close()
    return user_dict

