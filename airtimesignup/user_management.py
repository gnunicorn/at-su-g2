from airtimesignup.models import User
from airtimesignup.database import db_session


def get_user_from_browserid(user_data):
    if not user_data["status"] == "okay":
        raise ValueError(user_data)

    user = db_session.query(User
                            ).filter_by(email=user_data["email"]
                                        ).first()
    if not user:
        user = User(email=user_data["email"])
        db_session.add(user)
        db_session.commit()

    return user


def get_user_by_id(user_id):
    return db_session.query(User
                            ).filter_by(id=int(user_id)
                                        ).first()
