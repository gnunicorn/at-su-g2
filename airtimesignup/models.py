from airtimesignup.database import Base
from sqlalchemy import Column, Integer, Unicode, Sequence


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    fullname = Column(Unicode)
    email = Column(Unicode)
