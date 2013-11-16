from airtimesignup.database import Base
from sqlalchemy import Column, Integer, Unicode, Sequence


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    fullname = Column(Unicode)
    email = Column(Unicode)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id
